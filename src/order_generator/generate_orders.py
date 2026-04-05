import random
from datetime import timedelta
from src.utils.db_connection import get_db_connection


connection = get_db_connection()
cursor = connection.cursor()
cursor.execute("SELECT product_id, product_price FROM silver.products")
products = cursor.fetchall()

print(products)
