# ============================================
# Load Product Dimension (dim_product)
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
# Step 2: Select Product Columns
# --------------------------------------------
product_df = df[
    [
        "Product ID",
        "Product Name",
        "Category",
        "Sub-Category"
    ]
]

# --------------------------------------------
# Step 3: Remove Duplicate Products
# --------------------------------------------
product_df = product_df.drop_duplicates(subset=["Product ID"])

# --------------------------------------------
# Step 4: Verify the Data
# --------------------------------------------
print("========== Product Dimension Preview ==========")
print(product_df.head())

print("\n========== Shape ==========")
print(product_df.shape)

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
INSERT INTO dim_product (
    product_id,
    product_name,
    category,
    sub_category
)
VALUES (%s, %s, %s, %s);
"""

# --------------------------------------------
# Step 8: Insert Products
# --------------------------------------------
for _, row in product_df.iterrows():

    cursor.execute(
        insert_query,
        (
            row["Product ID"],
            row["Product Name"],
            row["Category"],
            row["Sub-Category"]
        )
    )

# --------------------------------------------
# Step 9: Commit Transaction
# --------------------------------------------
conn.commit()

print("Product Dimension loaded successfully!")

# --------------------------------------------
# Step 10: Close Database Resources
# --------------------------------------------
cursor.close()
conn.close()

print("Database connection closed successfully.")