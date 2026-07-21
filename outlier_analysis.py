import pandas as pd

# ------------------------------------------
# Load Dataset
# ------------------------------------------

file_path = "data/raw/sales.xlsx"

orders_df = pd.read_excel(
    file_path,
    sheet_name="Orders"
)

# ------------------------------------------
# Function to Detect Outliers
# ------------------------------------------

def detect_outliers(dataframe, column_name):

    print("\n" + "=" * 60)
    print(f"OUTLIER ANALYSIS : {column_name}")
    print("=" * 60)

    # Calculate Quartiles
    Q1 = dataframe[column_name].quantile(0.25)
    Q3 = dataframe[column_name].quantile(0.75)

    # Calculate IQR
    IQR = Q3 - Q1

    # Calculate Limits
    lower_limit = Q1 - (1.5 * IQR)
    upper_limit = Q3 + (1.5 * IQR)

    # Find Outliers
    outliers = dataframe[
        (dataframe[column_name] < lower_limit) |
        (dataframe[column_name] > upper_limit)
    ]

    # Print Results
    print(f"Q1           : {Q1:.2f}")
    print(f"Q3           : {Q3:.2f}")
    print(f"IQR          : {IQR:.2f}")
    print(f"Lower Limit  : {lower_limit:.2f}")
    print(f"Upper Limit  : {upper_limit:.2f}")
    print(f"Outliers     : {len(outliers)}")

    return outliers


# ------------------------------------------
# Analyze Columns
# ------------------------------------------

sales_outliers = detect_outliers(orders_df, "Sales")

profit_outliers = detect_outliers(orders_df, "Profit")

quantity_outliers = detect_outliers(orders_df, "Quantity")

discount_outliers = detect_outliers(orders_df, "Discount")