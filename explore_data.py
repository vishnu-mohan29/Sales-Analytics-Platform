import pandas as pd


def load_orders_data(file_path):
    """Load the Orders sheet from the Excel file."""
    return pd.read_excel(file_path, sheet_name="Orders")


def dataset_overview(df):
    print("=" * 50)
    print("DATASET OVERVIEW")
    print("=" * 50)

    print(f"Rows    : {df.shape[0]}")
    print(f"Columns : {df.shape[1]}")

    print("\nColumn Names:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)


def check_missing_values(df):
    print("\n" + "=" * 50)
    print("MISSING VALUES")
    print("=" * 50)

    print(df.isnull().sum())


def check_duplicates(df):
    print("\n" + "=" * 50)
    print("DUPLICATE RECORDS")
    print("=" * 50)

    print(f"Duplicate Rows: {df.duplicated().sum()}")


def descriptive_statistics(df):
    print("\n" + "=" * 50)
    print("DESCRIPTIVE STATISTICS")
    print("=" * 50)

    print(df.describe())


def main():
    file_path = "data/raw/sales.xlsx"

    orders_df = load_orders_data(file_path)

    dataset_overview(orders_df)
    check_missing_values(orders_df)
    check_duplicates(orders_df)
    descriptive_statistics(orders_df)


if __name__ == "__main__":
    main()