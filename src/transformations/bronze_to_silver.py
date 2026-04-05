from src.utils.db_connection import get_db_connection

sql_files = [
    "sql/transformations/bronze_to_silver_categories.sql",
    "sql/transformations/bronze_to_silver_customers.sql",
    "sql/transformations/bronze_to_silver_products.sql"
]

def insert_data_to_silver(files_list):
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