from src.utils.db_connection import get_db_connection

sql_files = [
    "sql/transformations/populate_gold_dim_date.sql",
    "sql/transformations/populate_gold_dim_products.sql",
    "sql/transformations/populate_gold_dim_customers.sql",
    "sql/transformations/populate_gold_fact_orders.sql"
]

def insert_data_to_gold(files_list):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        for file in files_list:
            with open(file, 'r') as f:
                sql = f.read()
                cursor.execute(sql)
                print(f"Executing SQL from {file}...")
        connection.commit()
        print("Data ingestion from silver to gold completed successfully.")
    except Exception as e:
        print(f"Error during data ingestion: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    insert_data_to_gold(sql_files)
