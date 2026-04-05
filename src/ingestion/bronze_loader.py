"""Bronze layer loader for raw API data ingestion.

Fetches data from the Platzi API and inserts it as raw JSON into
the bronze schema tables. Each run truncates and reloads, logging
success or failure to bronze.ingestion_log.
"""

from src.ingestion.api_client import get_api_data
from src.utils.db_connection import get_db_connection
from psycopg2.extras import Json
from datetime import datetime

source = "platzi_api"

table_config = [
    {"table_name": "bronze.categories_raw", "endpoint": "categories", "payload_column": "categories_payload"},
    {"table_name": "bronze.products_raw", "endpoint": "products", "payload_column": "products_payload"},
    {"table_name": "bronze.users_raw", "endpoint": "users", "payload_column": "users_payload"},
]

def insert_data_to_bronze(api_data, table_name, payload_column_name, source_name):
    """Truncate and reload a bronze table with raw API data.

    Each record is stored as a JSON payload alongside metadata (source,
    batch_id). The operation is logged to bronze.ingestion_log with
    either a 'success' or 'failure' status.

    Args:
        api_data: List of dicts representing the raw API response.
        table_name: Fully qualified bronze table name (e.g. "bronze.products_raw").
        payload_column_name: Name of the JSONB column to store the payload.
        source_name: Identifier for the data source (e.g. "platzi_api").
    """
    try:
        batch_id = datetime.now().isoformat()
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(f"TRUNCATE {table_name}")

        for row in api_data:
            cursor.execute(
                f"INSERT INTO {table_name} ({payload_column_name}, source, batch_id) VALUES (%s, %s, %s)",
                (Json(row), source_name, batch_id)
            )

        print(f"data inserted successfully in {table_name}")
        connection.commit()
        cursor.execute("INSERT INTO bronze.ingestion_log (source, batch_id, record_count, status, table_name) VALUES (%s, %s, %s, %s, %s)",
                       (source_name, batch_id, len(api_data), 'success', table_name))
        connection.commit()
    except Exception as e:
        print(f"Error inserting data {e}")
        cursor.execute("INSERT INTO bronze.ingestion_log (source, batch_id, record_count, status, table_name, error_message) VALUES (%s, %s, %s, %s, %s, %s)",
                       (source_name, batch_id, 0, 'failure', table_name, str(e)))
        connection.commit()
        
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    for table in table_config:
        data_json = get_api_data(table["endpoint"])
        if data_json:
            insert_data_to_bronze(data_json, table["table_name"], table["payload_column"], source)
        else:
            print(f"Skipping {table['table_name']} due to no data retrieved from API.")