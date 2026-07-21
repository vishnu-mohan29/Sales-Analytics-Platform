# ============================================
# Load Customer Dimension (dim_customer)
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
# Step 2: Select Customer Columns
# --------------------------------------------
customer_df = df[
    [
        "Customer ID",
        "Customer Name",
        "Segment"
    ]
]

# --------------------------------------------
# Step 3: Remove Duplicate Customers
# --------------------------------------------
customer_df = customer_df.drop_duplicates(subset=["Customer ID"])

# --------------------------------------------
# Step 4: Verify the Data
# --------------------------------------------
print("========== Customer Dimension Preview ==========")
print(customer_df.head())

print("\n========== Shape ==========")
print(customer_df.shape)

# --------------------------------------------
# Step 5: Connect to PostgreSQL
# --------------------------------------------
conn = create_connection()

# Check whether the connection was successful
if conn is None:
    print("Failed to connect to the database.")
    exit()

print("\nDatabase connection established successfully!")

# --------------------------------------------
# Step 6: Create a Cursor
# --------------------------------------------
cursor = conn.cursor()

print("Cursor created successfully.")


# --------------------------------------------
# Step 7: SQL Query for dim_customer
# --------------------------------------------
insert_query = """
INSERT INTO dim_customer (
    customer_id,
    customer_name,
    segment
)
VALUES (%s, %s, %s);
"""
# --------------------------------------------
# Step 8: Insert Customers
# --------------------------------------------
for index, row in customer_df.iterrows():

    cursor.execute(
        insert_query,
        (
            row["Customer ID"],
            row["Customer Name"],
            row["Segment"]
        )
    )
    
    # --------------------------------------------
# Step 9: Save Changes
# --------------------------------------------
conn.commit()

print("Customer Dimension loaded successfully!")

# --------------------------------------------
# Step 10: Close the Connection (Temporary)
# --------------------------------------------
cursor.close()
conn.close()

print("Database connection closed successfully.")
