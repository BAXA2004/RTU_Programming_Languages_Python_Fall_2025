# 1. Parse your CSV file
python flight_parser.py -i data/db.csv

# 2. Run queries on the generated database
python flight_parser.py -j db.json -q data/query.json

# 3. View your results
cat response_241ADB017_Bakhronjon_Hamzaev_*.json