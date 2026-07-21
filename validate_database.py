# ============================================
# Sales Analytics Platform
# Database Validation Script
# ============================================

from python.database.db_connection import create_connection


def validate_database():

    print("=" * 70)
    print("DATABASE VALIDATION")
    print("=" * 70)

    conn = create_connection()

    if conn is None:
        print("Failed to connect to PostgreSQL.")
        return

    cursor = conn.cursor()

    # --------------------------------------------
    # Tables to Validate
    # --------------------------------------------
    tables = [

        "dim_customer",

        "dim_product",

        "dim_location",

        "dim_ship_mode",

        "dim_date",

        "fact_sales"

    ]

    validation_success = True

    print(f"{'Table Name':<25}{'Record Count'}")
    print("-" * 40)

    for table in tables:

        try:

            cursor.execute(f"SELECT COUNT(*) FROM {table};")

            count = cursor.fetchone()[0]

            print(f"{table:<25}{count}")

            if count == 0:
                validation_success = False

        except Exception as e:

            validation_success = False

            print(f"{table:<25}ERROR")

            print(e)

    print("-" * 40)

    if validation_success:

        print("\nValidation Status : SUCCESS")

    else:

        print("\nValidation Status : FAILED")

    cursor.close()
    conn.close()

    print("\nDatabase connection closed.")


if __name__ == "__main__":

    validate_database()