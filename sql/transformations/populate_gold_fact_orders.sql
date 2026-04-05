INSERT INTO gold.fact_orders (order_id, dim_customer_key, dim_product_key, quantity, unit_price, total_price, order_date)
SELECT 
    so.order_id,
    gdc.dim_customer_key,
    gdp.dim_product_key,
    so.quantity,
    so.unit_price,
    so.total_price,
    so.order_date
FROM silver.orders so
JOIN gold.dim_customers gdc ON so.customer_id = gdc.customer_id
JOIN gold.dim_products gdp ON so.product_id = gdp.product_id
    AND so.order_date >= gdp.valid_from
    AND so.order_date < gdp.valid_to
WHERE so.order_id NOT IN (SELECT order_id FROM gold.fact_orders);