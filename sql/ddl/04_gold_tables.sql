CREATE TABLE IF NOT EXISTS gold.dim_date (
    date_id DATE PRIMARY KEY,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    day INTEGER,
    day_of_week INTEGER,
    is_weekend BOOLEAN,
    month_name TEXT,
    day_name TEXT
);


CREATE TABLE IF NOT EXISTS gold.dim_products (
    dim_product_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id INTEGER NOT NULL,
    product_name TEXT NOT NULL,
    product_slug TEXT NOT NULL,
    product_price NUMERIC(10,2) NOT NULL,
    valid_from TIMESTAMP NOT NULL,
    valid_to TIMESTAMP NOT NULL DEFAULT '2299-12-31 23:59:59',
    is_current BOOLEAN NOT NULL DEFAULT TRUE,
    product_description TEXT,
    product_category_id INTEGER,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);


CREATE TABLE IF NOT EXISTS gold.dim_customers (
    dim_customer_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id INTEGER NOT NULL UNIQUE,
    customer_name TEXT NOT NULL,
    customer_email TEXT NOT NULL UNIQUE,
    customer_role TEXT NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);


CREATE TABLE IF NOT EXISTS gold.fact_orders (
    fact_order_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id INTEGER NOT NULL,
    dim_customer_key INTEGER NOT NULL REFERENCES gold.dim_customers(dim_customer_key),
    dim_product_key INTEGER NOT NULL REFERENCES gold.dim_products(dim_product_key),
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(10,2) NOT NULL,
    total_price NUMERIC(10,2) NOT NULL,
    order_date DATE REFERENCES gold.dim_date(date_id)
);