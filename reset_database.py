# ============================================
# Reset PostgreSQL Database
# Clears all tables before ETL
# ============================================

from python.database.db_connection import create_connection


def reset_database():

    print("=" * 60)
    print("Resetting Database...")
    print("=" * 60)

    conn = create_connection()

    if conn is None:
        print("Failed to connect to PostgreSQL.")
        return False

    cursor = conn.cursor()

    try:

        # Disable foreign key checks temporarily
        cursor.execute("""
        TRUNCATE TABLE
            fact_sales,
            dim_customer,
            dim_product,
            dim_location,
            dim_ship_mode,
            dim_date
        RESTART IDENTITY CASCADE;
        """)

        conn.commit()

        print("Database reset completed successfully.")
        return True

    except Exception as e:

        conn.rollback()

        print("Error while resetting database.")
        print(e)

        return False

    finally:

        cursor.close()
        conn.close()


if __name__ == "__main__":
    reset_database()