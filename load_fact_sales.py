# ============================================
# Load Fact Table (fact_sales)
# ============================================

# --------------------------------------------
# Import Required Libraries
# --------------------------------------------
import pandas as pd
from python.database.db_connection import create_connection

# --------------------------------------------
# Step 1: Read the Cleaned Dataset
# --------------------------------------------
df = pd.read_csv("data/cleaned/sales_cleaned.csv")

# --------------------------------------------
# Step 2: Connect to PostgreSQL
# --------------------------------------------
conn = create_connection()

if conn is None:
    print("Failed to connect to the database.")
    exit()

cursor = conn.cursor()

print("Database connection established successfully!")

# --------------------------------------------
# Step 3: SQL Insert Query
# --------------------------------------------
insert_query = """
INSERT INTO fact_sales (
    order_id,
    customer_id,
    product_id,
    location_id,
    ship_mode_id,
    date_id,
    sales,
    quantity,
    discount,
    profit,
    shipping_days,
    profit_margin,
    loss_order
)
VALUES (%s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s);
"""

# --------------------------------------------
# Step 4: Loop Through Sales Records
# --------------------------------------------
for _, row in df.iterrows():

    print(row["Order ID"])

    # ----------------------------------------
    # Lookup location_id from dim_location
    # ----------------------------------------
    cursor.execute("""
        SELECT location_id
        FROM dim_location
        WHERE postal_code = %s
        AND city = %s
        AND state = %s
        AND region = %s
        AND country = %s;
    """, (
        row["Postal Code"],
        row["City"],
        row["State"],
        row["Region"],
        row["Country"]
    ))

    result = cursor.fetchone()
    location_id = result[0] if result else None

    # ----------------------------------------
    # Lookup ship_mode_id from dim_ship_mode
    # ----------------------------------------
    cursor.execute("""
        SELECT ship_mode_id
        FROM dim_ship_mode
        WHERE ship_mode = %s;
    """, (row["Ship Mode"],))

    result = cursor.fetchone()
    ship_mode_id = result[0] if result else None

    # ----------------------------------------
    # Lookup date_id from dim_date
    # ----------------------------------------
    cursor.execute("""
        SELECT date_id
        FROM dim_date
        WHERE order_date = %s;
    """, (row["Order Date"],))

    result = cursor.fetchone()
    date_id = result[0] if result else None

    # ----------------------------------------
    # Insert Record into fact_sales Table
    # ----------------------------------------
    cursor.execute(insert_query, (
        row["Order ID"],
        row["Customer ID"],
        row["Product ID"],
        location_id,
        ship_mode_id,
        date_id,
        row["Sales"],
        row["Quantity"],
        row["Discount"],
        row["Profit"],
        row["Shipping Days"],
        row["Profit Margin"],
        row["Loss Order"]
    ))

# --------------------------------------------
# Step 5: Commit Transaction
# --------------------------------------------
conn.commit()

print("Fact table loaded successfully!")

# --------------------------------------------
# Step 6: Close Database Resources
# --------------------------------------------
cursor.close()
conn.close()

print("Database connection closed successfully.")