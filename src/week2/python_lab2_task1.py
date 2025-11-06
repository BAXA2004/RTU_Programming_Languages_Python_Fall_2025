"""
Lab 3.1 – Simple Datasets and Aggregates

Goals:
- Create and manipulate Python lists and dictionaries.
- Compute aggregates such as sum, average, max, and min.

Instructions:
1. Create a list `temperatures` with daily temperatures for one week.
2. Create a dictionary `city_population` with at least 5 cities and their populations.
3. Compute:
   - The average temperature.
   - The maximum and minimum population.
   - The total population of all cities.
4. Print your results in a clear, formatted way.
"""

# TODO: Create the datasets - up to you to fill in the data
temperatures = [22.5, 18.3, 25.7, 15.2, 28.9, 19.8, 23.1]  # 7 days for one week
city_population = {
    "Samarkand": 546000,
    "Andijan": 458000,
    "Navoiy": 134000,
    "Buxoro": 285000,
    "Jizzax": 179000,
    "Toshkent": 2570000,
    "Namangan": 626000
}

# TODO: Compute aggregates
average_temperature = sum(temperatures) / len(temperatures)
largest_city = max(city_population, key=city_population.get)
largest_population = city_population[largest_city]
smallest_city = min(city_population, key=city_population.get)
smallest_population = city_population[smallest_city]
total_population = sum(city_population.values())

# TODO: Print results
print("Average temperature:", round(average_temperature, 2))
print("Largest city:", largest_city, "-", largest_population)
print("Smallest city:", smallest_city, "-", smallest_population)
print("Total population:", total_population)