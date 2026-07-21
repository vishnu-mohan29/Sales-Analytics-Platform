import pandas as pd

# ==========================================
# Script : feature_engineering.py
# Purpose: Create new features for analysis
# Project: Sales Analytics Platform
# ==========================================

# Load Dataset
file_path = "data/raw/sales.xlsx"

orders_df = pd.read_excel(
    file_path,
    sheet_name="Orders",
    parse_dates=["Order Date", "Ship Date"]
)

print("Dataset Loaded Successfully")
print(f"Rows : {len(orders_df)}")

# Create Order Year
orders_df["Order Year"] = orders_df["Order Date"].dt.year

# Create Order Month
orders_df["Order Month"] = orders_df["Order Date"].dt.month_name()

# Create Month Number
orders_df["Month Number"] = orders_df["Order Date"].dt.month

#Quarter
orders_df["Quarter"] = "Q" + orders_df["Order Date"].dt.quarter.astype(str)

#Day Name
orders_df["Day Name"] = orders_df["Order Date"].dt.day_name()

#Shipping Days
orders_df["Shipping Days"] = (orders_df["Ship Date"] - orders_df["Order Date"]).dt.days

#Profit Margin
orders_df["Profit Margin"] = ((orders_df["Profit"] / orders_df["Sales"]) * 100).round(2)

#Loss Order
orders_df["Loss Order"] = orders_df["Profit"].apply(lambda x: "Yes" if x < 0 else "No")


print("\nNew Features Created Successfully!\n")

print(orders_df[[
            "Order Year",
            "Order Month",
            "Month Number",
            "Quarter",
            "Day Name",
            "Shipping Days",
            "Profit Margin",
            "Loss Order"]].head())

# Save cleaned dataset

output_path = "data/cleaned/sales_cleaned.xlsx"
csv_path = "data/cleaned/sales_cleaned.csv"
orders_df.to_excel(output_path, index=False)

orders_df.to_csv("data/cleaned/sales_cleaned.csv",index=False)

print("\n" + "=" * 60)
print("DATASET SAVED SUCCESSFULLY")
print("=" * 60)
print(f"Location : {output_path}")
print(f"CSV File   : {csv_path}")
