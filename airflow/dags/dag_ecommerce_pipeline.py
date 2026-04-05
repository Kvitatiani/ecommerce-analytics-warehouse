"""Airflow DAG for the full ecommerce medallion pipeline.

Orchestrates the daily pipeline: bronze ingestion from the API,
silver cleansing/transformation, and gold dimensional model population.
Tasks run sequentially: bronze -> silver -> gold.
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
sys.path.insert(0, '/opt/airflow')

from src.ingestion.bronze_loader import insert_data_to_bronze, table_config, source
from src.ingestion.api_client import get_api_data
from src.transformations.bronze_to_silver import insert_data_to_silver, sql_files as silver_sql_files
from src.transformations.silver_to_gold import insert_data_to_gold, sql_files as gold_sql_files

def run_bronze_ingestion():
    """Ingest all configured API endpoints into bronze schema tables.

    Iterates over table_config and, for each entry, fetches data from
    the API and loads it into the corresponding bronze table.
    """
    for table in table_config:
        data_json = get_api_data(table["endpoint"])
        if data_json:
            insert_data_to_bronze(data_json, table["table_name"], table["payload_column"], source)

def run_silver_ingestion():
    """Run all bronze-to-silver SQL transformation scripts."""
    insert_data_to_silver(silver_sql_files)

def run_gold_ingestion():
    """Run all silver-to-gold SQL population scripts."""
    insert_data_to_gold(gold_sql_files)


with DAG(
    dag_id='ecommerce_pipeline',
    start_date=datetime(2026, 4, 1),
    schedule='@daily',
    catchup=False
) as dag:
    # define tasks here
    bronze_task = PythonOperator(
        task_id='bronze_ingestion',
        python_callable=run_bronze_ingestion
    )

    silver_task = PythonOperator(
        task_id='silver_ingestion',
        python_callable=run_silver_ingestion
    )
    gold_task = PythonOperator(
        task_id='gold_ingestion',
        python_callable=run_gold_ingestion
    )

    bronze_task >> silver_task >> gold_task
