"""Database connection utility for the ecommerce analytics warehouse.

Loads PostgreSQL credentials from environment variables and provides
a reusable connection factory for all pipeline stages.
"""

from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

db_host = os.getenv("POSTGRES_HOST")
db_port = os.getenv("POSTGRES_PORT")
db_name = os.getenv("POSTGRES_DB")
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")

def get_db_connection():
    """Create and return a new PostgreSQL database connection.

    Reads connection parameters (host, port, dbname, user, password) from
    environment variables loaded at module import time.

    Returns:
        psycopg2.extensions.connection: An open database connection,
            or None if the connection attempt fails.
    """
    try:
        connection = psycopg2.connect(
            host = db_host,
            port = db_port,
            dbname = db_name,
            user = db_user,
            password = db_password
        )
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        print("Database connection successful")
        conn.close()
    else:
        print("Database connection failed")