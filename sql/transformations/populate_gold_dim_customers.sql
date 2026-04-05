INSERT INTO gold.dim_customers(customer_id, customer_name, customer_email, customer_role, created_at, updated_at)
SELECT customer_id, customer_name, customer_email, customer_role, created_at, updated_at
FROM silver.customers
ON CONFLICT (customer_id) DO UPDATE SET
    customer_email = EXCLUDED.customer_email,
    customer_name = EXCLUDED.customer_name,
    customer_role = EXCLUDED.customer_role,
    created_at = EXCLUDED.created_at,
    updated_at = EXCLUDED.updated_at;