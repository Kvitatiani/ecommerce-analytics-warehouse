import random
from datetime import timedelta, datetime, date
from src.utils.db_connection import get_db_connection


def generate_orders():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # fetch product ids and prices from silver layer
        cursor.execute("SELECT product_id, product_price FROM silver.products")
        products = cursor.fetchall()

        # fetching customer ids from silver layer
        cursor.execute("SELECT customer_id FROM silver.customers")
        customers = cursor.fetchall()

        # Generating orders for the last 6 months
        date_range_start = date(2025, 10, 1)
        date_range_end = date.today()

        # set order_id to 0, it will be incremented for each new order
        order_id = 0

        # Generating orders for each day in the date range
        for day in range((date_range_end - date_range_start).days + 1):
            order_date = date_range_start + timedelta(days=day)
            for order in range(random.randint(10,50)):
                customer = random.choice(customers)
                num_distinct_products = random.randint(1, 5)
                order_id += 1
                for line_item in range(num_distinct_products):
                    product = random.choice(products)
                    product_quantity = random.randint(1, 3)
                    total_price = product[1] * product_quantity
                    cursor.execute(
                        "INSERT INTO silver.orders (order_id, customer_id, order_date, product_id, quantity, unit_price, total_price) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (order_id, customer[0], order_date, product[0], product_quantity, product[1], total_price)
                    )
        connection.commit()
        print("Orders generated and inserted into silver.orders successfully.")
    except Exception as e:
        connection.rollback()
        print(f"Error generating orders: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    generate_orders()
