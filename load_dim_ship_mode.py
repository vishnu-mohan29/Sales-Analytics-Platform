# ============================================
# Load Ship Mode Dimension (dim_ship_mode)
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
# Step 2: Select Ship Mode Column
# --------------------------------------------
ship_mode_df = df[
    [
        "Ship Mode"
    ]
]

# --------------------------------------------
# Step 3: Remove Duplicate Ship Modes
# --------------------------------------------
ship_mode_df = ship_mode_df.drop_duplicates()

# --------------------------------------------
# Step 4: Verify the Data
# --------------------------------------------
print("========== Ship Mode Dimension Preview ==========")
print(ship_mode_df.head())

print("\n========== Shape ==========")
print(ship_mode_df.shape)

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
INSERT INTO dim_ship_mode (
    ship_mode
)
VALUES (%s);
"""

# --------------------------------------------
# Step 8: Insert Ship Modes
# --------------------------------------------
for _, row in ship_mode_df.iterrows():

    cursor.execute(
        insert_query,
        (
            row["Ship Mode"],
        )
    )

# --------------------------------------------
# Step 9: Commit Transaction
# --------------------------------------------
conn.commit()

print("Ship Mode Dimension loaded successfully!")

# --------------------------------------------
# Step 10: Close Database Resources
# --------------------------------------------
cursor.close()
conn.close()

print("Database connection closed successfully.")