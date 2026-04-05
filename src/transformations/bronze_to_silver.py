"""Bronze-to-silver transformation layer.

Reads SQL transformation files that extract, clean, and deduplicate
raw JSON data from the bronze schema into typed, structured tables
in the silver schema.
"""

from src.utils.db_connection import get_db_connection

sql_files = [
    "sql/transformations/bronze_to_silver_categories.sql",
    "sql/transformations/bronze_to_silver_customers.sql",
    "sql/transformations/bronze_to_silver_products.sql"
]

def insert_data_to_silver(files_list):
    """Execute SQL transformation files to populate the silver schema.

    Opens each SQL file in order, executes it against the database, and
    commits the transaction once all files succeed.

    Args:
        files_list: List of file paths to SQL transformation scripts
            (e.g. bronze-to-silver UPSERT queries).
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        for file in files_list:
            with open(file, 'r') as f:
                sql = f.read()
                cursor.execute(sql)
                print(f"Executing SQL from {file}...")
        connection.commit()
        print("Data transformation from bronze to silver completed successfully.")
    except Exception as e:
        print(f"Error during data transformation: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    insert_data_to_silver(sql_files)