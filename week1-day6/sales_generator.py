from faker import Faker
import pandas as pd
import random
from datetime import date

fake = Faker()

products = [
    "Laptop",
    "Mouse",
    "Keyboard",
    "Monitor",
    "USB Cable"
]

countries = [
    "USA",
    "UK",
    "Germany",
    "France",
    "Japan"
]

sales = []

for order_id in range(1, 101):
    sale = {
        "order_id": order_id,
        "customer_name": fake.name(),
        "product": random.choice(products),
        "quantity": random.randint(1, 10),
        "price": round(random.uniform(10.00, 500.00), 2),
        "order_date": fake.date_between(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31)
        ),
        "country": random.choice(countries)
    }

    sales.append(sale)

df = pd.DataFrame(sales)

df.to_csv("raw_sales.csv", index=False)

print(df.head())
print(f"\nGenerated {len(df)} sales records.")