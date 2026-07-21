import psycopg2


def create_connection():
    """
    Create and return a connection to the PostgreSQL database.
    """

    try:
        connection = psycopg2.connect(
            host="localhost",
            database="sales_analytics",
            user="postgres",
            password="Admin@123",
            port="5432"
        )

        print(" Connected to PostgreSQL successfully!")

        return connection

    except Exception as error:
        print("Database connection failed.")
        print(error)

        return None
    # Test the database connection
if __name__ == "__main__":
    connection = create_connection()

    if connection:
        connection.close()
        print("Connection closed successfully.")