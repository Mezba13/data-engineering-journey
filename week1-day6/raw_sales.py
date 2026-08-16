import pandas as pd

# ==========================================
# 1. READ RAW DATA
# ==========================================

df = pd.read_csv("raw_sales.csv")

print("Raw data:")
print(df.head())


# ==========================================
# 2. CLEAN AND TRANSFORM
# ==========================================

# Calculate total amount
df["total_amount"] = df["quantity"] * df["price"]


# Add discount
# 10% discount if quantity > 5
# Otherwise 0%

df["discount"] = df["quantity"].apply(
    lambda x: 0.10 if x > 5 else 0
)


# Calculate final amount
df["final_amount"] = (
    df["total_amount"] * (1 - df["discount"])
)


# Standardize customer names
df["customer_name"] = df["customer_name"].str.upper()


# Convert order_date to datetime
df["order_date"] = pd.to_datetime(df["order_date"])


# ==========================================
# 3. VALIDATE DATA
# ==========================================

# Check required columns for nulls
required_columns = [
    "order_id",
    "customer_name",
    "product"
]

for column in required_columns:
    assert df[column].notna().all(), (
        f"Validation failed: {column} contains nulls"
    )


# Quantity must be greater than 0
assert (df["quantity"] > 0).all(), (
    "Validation failed: quantity must be greater than 0"
)


# Price must be greater than 0
assert (df["price"] > 0).all(), (
    "Validation failed: price must be greater than 0"
)


print("\nValidation successful!")


# ==========================================
# 4. ANALYSIS
# ==========================================

# Total revenue
total_revenue = df["final_amount"].sum()


# Top 3 products by revenue
top_products = (
    df.groupby("product")["final_amount"]
    .sum()
    .sort_values(ascending=False)
    .head(3)
)


# Top 3 countries by order count
top_countries = (
    df["country"]
    .value_counts()
    .head(3)
)


# Average order value
average_order_value = df["final_amount"].mean()


# ==========================================
# 5. PRINT ANALYSIS
# ==========================================

print("\n========== SALES REPORT ==========")

print(f"\nTotal Revenue: ${total_revenue:,.2f}")

print("\nTop 3 Products by Revenue:")
print(top_products)

print("\nTop 3 Countries by Order Count:")
print(top_countries)

print(f"\nAverage Order Value: ${average_order_value:,.2f}")


# ==========================================
# 6. EXPORT CLEAN DATA
# ==========================================

df.to_csv("clean_sales.csv", index=False)

print("\nClean data saved to clean_sales.csv")


# ==========================================
# 7. CREATE SALES REPORT
# ==========================================

with open("sales_report.txt", "w", encoding="utf-8") as f:

    f.write("========== SALES REPORT ==========\n\n")

    f.write(
        f"Total Revenue: ${total_revenue:,.2f}\n\n"
    )

    f.write("Top 3 Products by Revenue:\n")

    for product, revenue in top_products.items():
        f.write(
            f"{product}: ${revenue:,.2f}\n"
        )

    f.write("\nTop 3 Countries by Order Count:\n")

    for country, count in top_countries.items():
        f.write(
            f"{country}: {count} orders\n"
        )

    f.write(
        f"\nAverage Order Value: "
        f"${average_order_value:,.2f}\n"
    )

print("Sales report saved to sales_report.txt")