# ============================================
# Load Date Dimension (dim_date)
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
# Step 2: Select Date Columns
# --------------------------------------------
date_df = df[
    [
        "Order Date",
        "Order Year",
        "Order Month",
        "Month Number",
        "Quarter",
        "Day Name"
    ]
]

# --------------------------------------------
# Step 3: Remove Duplicate Dates
# --------------------------------------------
date_df = date_df.drop_duplicates(subset=["Order Date"])

# --------------------------------------------
# Step 4: Verify the Data
# --------------------------------------------
print("========== Date Dimension Preview ==========")
print(date_df.head())

print("\n========== Shape ==========")
print(date_df.shape)

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
INSERT INTO dim_date (
    order_date,
    order_year,
    order_month,
    month_number,
    quarter,
    day_name
)
VALUES (%s, %s, %s, %s, %s, %s);
"""

# --------------------------------------------
# Step 8: Insert Dates
# --------------------------------------------
for _, row in date_df.iterrows():

    cursor.execute(
        insert_query,
        (
            row["Order Date"],
            row["Order Year"],
            row["Order Month"],
            row["Month Number"],
            row["Quarter"],
            row["Day Name"]
        )
    )

# --------------------------------------------
# Step 9: Commit Transaction
# --------------------------------------------
conn.commit()

print("Date Dimension loaded successfully!")

# --------------------------------------------
# Step 10: Close Database Resources
# --------------------------------------------
cursor.close()
conn.close()

print("Database connection closed successfully.")