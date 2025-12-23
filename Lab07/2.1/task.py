import csv

data_with = []

with open(r'D:\SL_LABS\Lab07\2.1\2.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        data_with.append(row)
        for key, value in row.items():
            print(f"  {key} -> {value}")


def find_min_max_quantity_order(data):
    quantities = [int(row['Quantity']) for row in data]
    min_q = min(quantities)
    max_q = max(quantities)
    return min_q, max_q

def calculate_total_revenue(data):
    total = sum(int(row['Quantity']) * float(row['Price']) for row in data)
    return total

def calculate_average_quantity(data):
    quantities = [int(row['Quantity']) for row in data]
    avg = sum(quantities) / len(quantities)
    return avg

def count_orders_by_country(data):
    country_count = {}
    for row in data:
        country = row['Country']
        country_count[country] = country_count.get(country, 0) + 1
    return country_count

min_q, max_q = find_min_max_quantity_order(data_with)
print(f"Минимальное количество: {min_q}, Максимальное количество: {max_q}")

total_revenue = calculate_total_revenue(data_with)
print(f"Общая выручка: {total_revenue}")

avg_quantity = calculate_average_quantity(data_with)
print(f"Среднее количество: {avg_quantity}")

orders_by_country = count_orders_by_country(data_with)
for country, count in orders_by_country.items():
    print(f"{country} -> {count}")