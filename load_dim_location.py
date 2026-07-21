# ============================================
# Load Location Dimension (dim_location)
# ============================================

# --------------------------------------------
# Import Required Libraries
# --------------------------------------------
import pandas as pd

# Import the database connection function
from python.database.db_connection import create_connection

# --------------------------------------------
# Step 1: Read the Cleaned Dataset
# --------------------------------------------
df = pd.read_csv("data/cleaned/sales_cleaned.csv")

# --------------------------------------------
# Step 2: Select Location Columns
# --------------------------------------------
location_df = df[
    [
        "Postal Code",
        "City",
        "State",
        "Region",
        "Country"
    ]
]

# --------------------------------------------
# Step 3: Remove Duplicate Locations
# --------------------------------------------
location_df = location_df.drop_duplicates()

# --------------------------------------------
# Step 4: Verify the Data
# --------------------------------------------
print("========== Location Dimension Preview ==========")
print(location_df.head())

print("\n========== Shape ==========")
print(location_df.shape)

# --------------------------------------------
# Step 5: Connect to PostgreSQL
# --------------------------------------------
conn = create_connection()

if conn is None:
    print("Failed to connect to the database.")
    exit()

print("\nDatabase connection established successfully!")

# --------------------------------------------
# Step 6: Create Cursor
# --------------------------------------------
cursor = conn.cursor()

print("Cursor created successfully.")

# --------------------------------------------
# Step 7: SQL Query
# --------------------------------------------
insert_query = """
INSERT INTO dim_location (
    postal_code,
    city,
    state,
    region,
    country
)
VALUES (%s, %s, %s, %s, %s);
"""

# --------------------------------------------
# Step 8: Insert Locations
# --------------------------------------------
for _, row in location_df.iterrows():

    cursor.execute(
        insert_query,
        (
            row["Postal Code"],
            row["City"],
            row["State"],
            row["Region"],
            row["Country"]
        )
    )

# --------------------------------------------
# Step 9: Commit Transaction
# --------------------------------------------
conn.commit()

print("Location Dimension loaded successfully!")

# --------------------------------------------
# Step 10: Close Database Resources
# --------------------------------------------
cursor.close()
conn.close()

print("Database connection closed successfully.")