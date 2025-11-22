#!/usr/bin/env python3
"""
Flight Schedule Parser and Query Tool
"""

import argparse
import csv
import json
import os
import re
from datetime import datetime
from pathlib import Path


class FlightValidator:
    @staticmethod
    def validate_flight_id(flight_id):
        return bool(re.match(r"^[A-Za-z0-9]{2,8}$", flight_id))

    @staticmethod
    def validate_airport_code(code):
        return bool(re.match(r"^[A-Z]{3}$", code))

    @staticmethod
    def validate_datetime(dt_string):
        try:
            datetime.strptime(dt_string, "%Y-%m-%d %H:%M")
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_price(price):
        try:
            price_float = float(price)
            return price_float > 0
        except ValueError:
            return False

    @staticmethod
    def validate_times(departure, arrival):
        try:
            dep_dt = datetime.strptime(departure, "%Y-%m-%d %H:%M")
            arr_dt = datetime.strptime(arrival, "%Y-%m-%d %H:%M")
            return arr_dt > dep_dt
        except ValueError:
            return False


class FlightParser:
    def __init__(self):
        self.validator = FlightValidator()
        self.valid_flights = []
        self.errors = []

    def parse_csv_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()

            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                self.process_line(line, line_num, file_path)

        except Exception as e:
            self.errors.append(f"Error reading file {file_path}: {e}")

    def process_line(self, line, line_num, file_path):
        try:
            fields = line.split(",")

            if len(fields) != 6:
                self.errors.append(
                    f"Line {line_num}: {line} → incorrect number of fields"
                )
                return

            flight_id, origin, destination, dep_time, arr_time, price = fields

            validation_errors = []

            if not self.validator.validate_flight_id(flight_id):
                validation_errors.append("invalid flight_id")

            if not self.validator.validate_airport_code(origin):
                validation_errors.append("invalid origin code")

            if not self.validator.validate_airport_code(destination):
                validation_errors.append("invalid destination code")

            if not self.validator.validate_datetime(dep_time):
                validation_errors.append("invalid departure datetime")

            if not self.validator.validate_datetime(arr_time):
                validation_errors.append("invalid arrival datetime")
            elif not self.validator.validate_times(dep_time, arr_time):
                validation_errors.append("arrival before departure")

            if not self.validator.validate_price(price):
                validation_errors.append("invalid price")

            if validation_errors:
                error_msg = " → " + ", ".join(validation_errors)
                self.errors.append(f"Line {line_num}: {line}{error_msg}")
            else:
                flight_data = {
                    "flight_id": flight_id,
                    "origin": origin,
                    "destination": destination,
                    "departure_datetime": dep_time,
                    "arrival_datetime": arr_time,
                    "price": float(price),
                }
                self.valid_flights.append(flight_data)

        except Exception as e:
            self.errors.append(f"Line {line_num}: {line} → processing error: {e}")

    def parse_directory(self, directory_path):
        csv_files = list(Path(directory_path).glob("*.csv"))

        if not csv_files:
            print(f"No CSV files found in {directory_path}")
            return

        for csv_file in csv_files:
            print(f"Processing {csv_file}...")
            self.parse_csv_file(csv_file)

    def save_valid_flights(self, output_path):
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.valid_flights, f, indent=2)
        print(f"Saved {len(self.valid_flights)} valid flights to {output_path}")

    def save_errors(self, output_path):
        with open(output_path, "w", encoding="utf-8") as f:
            for error in self.errors:
                f.write(error + "\n")
        print(f"Saved {len(self.errors)} errors to {output_path}")


class QueryEngine:
    def __init__(self, database):
        self.database = database

    def execute_query(self, query):
        matches = []

        for flight in self.database:
            match = True

            for field, value in query.items():
                if field == "flight_id":
                    if flight.get("flight_id") != value:
                        match = False
                        break
                elif field == "origin":
                    if flight.get("origin") != value:
                        match = False
                        break
                elif field == "destination":
                    if flight.get("destination") != value:
                        match = False
                        break
                elif field == "departure_datetime":
                    flight_dt = datetime.strptime(
                        flight["departure_datetime"], "%Y-%m-%d %H:%M"
                    )
                    query_dt = datetime.strptime(value, "%Y-%m-%d %H:%M")
                    if flight_dt < query_dt:
                        match = False
                        break
                elif field == "arrival_datetime":
                    flight_dt = datetime.strptime(
                        flight["arrival_datetime"], "%Y-%m-%d %H:%M"
                    )
                    query_dt = datetime.strptime(value, "%Y-%m-%d %H:%M")
                    if flight_dt > query_dt:
                        match = False
                        break
                elif field == "price":
                    if flight.get("price") > float(value):
                        match = False
                        break

            if match:
                matches.append(flight)

        return matches

    def execute_queries(self, queries):
        results = []

        if isinstance(queries, dict):
            queries = [queries]

        for query in queries:
            matches = self.execute_query(query)
            results.append({"query": query, "matches": matches})

        return results


def load_json_database(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_query_results(
    results, student_id="241ADB017", name="Bakhronjon", lastname="Hamzaev"
):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"response_{student_id}_{name}_{lastname}_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"Query results saved to {filename}")
    return filename


def main():
    parser = argparse.ArgumentParser(
        description="Flight Schedule Parser and Query Tool"
    )
    parser.add_argument("-i", "--input", help="Parse a single CSV file")
    parser.add_argument("-d", "--directory", help="Parse all CSV files in a folder")
    parser.add_argument(
        "-o", "--output", help="Output JSON file for valid flights", default="db.json"
    )
    parser.add_argument("-j", "--json", help="Load existing JSON database")
    parser.add_argument("-q", "--query", help="Execute queries from JSON file")

    args = parser.parse_args()

    database = []

    if args.json:
        print(f"Loading existing database from {args.json}")
        database = load_json_database(args.json)
    elif args.input or args.directory:
        flight_parser = FlightParser()

        if args.input:
            print(f"Parsing CSV file: {args.input}")
            flight_parser.parse_csv_file(args.input)
        elif args.directory:
            print(f"Parsing CSV files in directory: {args.directory}")
            flight_parser.parse_directory(args.directory)

        database = flight_parser.valid_flights

        flight_parser.save_valid_flights(args.output)
        flight_parser.save_errors("errors.txt")

        print(
            f"Parsing complete: {len(database)} valid flights, {len(flight_parser.errors)} errors"
        )
    else:
        print(
            "Please specify input file (-i), directory (-d), or existing JSON database (-j)"
        )
        return

    if args.query:
        print(f"Executing queries from {args.query}")

        with open(args.query, "r", encoding="utf-8") as f:
            queries = json.load(f)

        query_engine = QueryEngine(database)
        results = query_engine.execute_queries(queries)

        output_file = save_query_results(results)
        print(f"Query execution complete. Results saved to {output_file}")


if __name__ == "__main__":
    main()
