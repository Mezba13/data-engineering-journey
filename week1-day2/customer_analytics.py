customers = [
    {"name": "Alice", "age": 34, "city": "New York", "spend": 250.50},
    {"name": "Bob", "age": 28, "city": "Los Angeles", "spend": 89.00},
    {"name": "Charlie", "age": 45, "city": "New York", "spend": 450.75},
    {"name": "Diana", "age": 31, "city": "Chicago", "spend": 120.00},
    {"name": "Evan", "age": 38, "city": "Los Angeles", "spend": 310.25},
    {"name": "Fiona", "age": 29, "city": "New York", "spend": 75.50},
    {"name": "George", "age": 42, "city": "Chicago", "spend": 199.99},
    {"name": "Hannah", "age": 26, "city": "Miami", "spend": 55.00},
    {"name": "Ian", "age": 50, "city": "Los Angeles", "spend": 520.00},
    {"name": "Julia", "age": 33, "city": "Miami", "spend": 180.00},
]

# print("=== High Spenders (>$100) ===")
# for c in customers:
#     if c["spend"] > 100:
#         print(f"{c['name']}: ${c['spend']}")

# print("\n=== Customers by City ===")
# city_counts = {}
# for c in customers:
#     city_counts[c["city"]] = city_counts.get(c["city"], 0) + 1
# for city, count in city_counts.items():
#     print(f"{city}: {count}")

# print("\n=== Highest Spender ===")
# highest = customers[0]
# for c in customers:
#     if c["spend"] > highest["spend"]:
#         highest = c
# print(f"{highest['name']} spent ${highest['spend']}")

# total = sum(c["spend"] for c in customers)
# print(f"\n=== Average Spend: ${total/len(customers):.2f} ===")

customers.append({"name": "Mezba", "age": 27, "city": "Dhaka", "spend": 300.00})
for c in customers:
    if c['age']>=30 and c['age']<=40:
        print(f"{c['name']} is between 30 and 40 years old.")

print("\n=== Customers with lowest spending ===")

lowest_spender=min(c['spend'] for c in customers)
print(lowest_spender)


print("\n=== Customers with lowest spending using lambda ===")
lowest_spender = min(customers, key=lambda c: c['spend'])
print(f"{lowest_spender['name']} spent ${lowest_spender['spend']}")