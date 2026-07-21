import pandas as pd

# Load the cleaned dataset
file_path = "data/cleaned/sales_cleaned.csv"

orders_df = pd.read_csv(file_path)

print("Dataset Loaded Successfully!")

print("=" * 60)
print("Missing Postal Codes")
print("=" * 60)

missing_postal_codes = orders_df["Postal Code"].isnull().sum()

print(f"Missing Postal Codes: {missing_postal_codes}")

print("\n" + "=" * 60)
print("Unique Postal Codes")
print("=" * 60)

unique_postal_codes = orders_df["Postal Code"].nunique()

print(f"Unique Postal Codes: {unique_postal_codes}")

print("\n" + "=" * 60)
print("Duplicate Postal Codes")
print("=" * 60)

duplicate_postal_codes = orders_df["Postal Code"].duplicated().sum()

print(f"Duplicate Postal Codes: {duplicate_postal_codes}")


# Check whether a postal code maps to more than one location

location_check = (
    orders_df.groupby("Postal Code")[["City", "State", "Region", "Country"]]
    .nunique()
)

print(location_check.head())

print("\nPostal codes with multiple locations:")

conflicts = location_check[
    (location_check["City"] > 1) |
    (location_check["State"] > 1) |
    (location_check["Region"] > 1) |
    (location_check["Country"] > 1)
]

print(conflicts)

print(f"\nNumber of conflicting postal codes: {len(conflicts)}")

orders_df[orders_df["Postal Code"] == 92024][
    ["City", "State", "Region", "Country", "Postal Code"]
].drop_duplicates()

orders_df[orders_df["Postal Code"] == 92024][
    ["City", "State", "Region", "Country", "Postal Code"]
].drop_duplicates()

print("=" * 60)
print("Conflicting Location Details")
print("=" * 60)

conflicting_locations = (
    orders_df[orders_df["Postal Code"] == 92024]
    [["Postal Code", "City", "State", "Region", "Country"]]
    .drop_duplicates()
)

print(conflicting_locations)