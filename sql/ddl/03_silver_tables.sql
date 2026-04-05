CREATE TABLE IF NOT EXISTS silver.categories (
    category_id INTEGER PRIMARY KEY,
    category_name TEXT NOT NULL,
    category_slug TEXT NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);


CREATE TABLE IF NOT EXISTS silver.products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    product_slug TEXT NOT NULL,
    product_price NUMERIC(10,2) NOT NULL,
    product_description TEXT,
    product_category_id INTEGER REFERENCES silver.categories(category_id),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);


CREATE TABLE IF NOT EXISTS silver.customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    customer_email TEXT NOT NULL UNIQUE,
    customer_role TEXT NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);