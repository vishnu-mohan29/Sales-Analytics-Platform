# ==========================================
# Script: business_rule_validation.py
# Purpose: Validate business rules on the sales dataset
# Project: Sales Analytics Platform
# ==========================================

import pandas as pd

file_path = "data/raw/sales.xlsx"

excel_file = pd.ExcelFile(file_path)

print("Available Sheets:")
print(excel_file.sheet_names)

# Load the Orders sheet
orders_df = pd.read_excel(file_path, sheet_name="Orders")

def print_section(title):
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)


print_section("Negative Sales")
negative_sales = orders_df[orders_df["Sales"] < 0]
print(f"Number of Negative Sales Records : {len(negative_sales)}")


print_section("Negative Quantity")
negative_quantity = orders_df[orders_df["Quantity"] <= 0]
print(f"Number of Negative quantity Records : {len(negative_quantity)}")


print_section("Negative profit")
negative_profit = orders_df[orders_df["Profit"] < 0]
print(f"Number of Negative profit Records : {len(negative_profit)}")


print_section("Ship Date Before Order Date")
invalid_shipping = orders_df[orders_df["Ship Date"] < orders_df["Order Date"]]
print(f"Orders Shipped Before Ordering : {len(invalid_shipping)}")


print_section("Invalid discount")
invalid_discount = orders_df[(orders_df["Discount"] < 0) | (orders_df["Discount"] > 1)]
print(f"Number of invalid discount Records : {len(invalid_discount)}")
