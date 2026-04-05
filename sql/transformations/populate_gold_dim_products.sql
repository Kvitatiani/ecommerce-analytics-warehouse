INSERT INTO gold.dim_products (product_id, product_name, product_slug, product_price, valid_from, valid_to, is_current, product_description, product_category_id, created_at, updated_at)
SELECT product_id, product_name, product_slug, product_price, NOW(), '2299-12-31 23:59:59', TRUE, product_description, product_category_id, created_at, updated_at
FROM silver.products sp
WHERE sp.product_id NOT IN (SELECT product_id FROM gold.dim_products);

UPDATE gold.dim_products
SET is_current = FALSE, valid_to = NOW()
WHERE is_current = TRUE
AND product_id IN (SELECT sp.product_id
                   FROM silver.products sp
                   JOIN gold.dim_products gdp ON sp.product_id = gdp.product_id
                   WHERE sp.product_price != gdp.product_price
                   AND gdp.is_current = TRUE);

INSERT INTO gold.dim_products (product_id, product_name, product_slug, product_price, valid_from, valid_to, is_current, product_description, product_category_id, created_at, updated_at)
SELECT product_id, product_name, product_slug, product_price, NOW(), '2299-12-31 23:59:59', TRUE, product_description, product_category_id, created_at, updated_at
FROM silver.products sp
WHERE sp.product_id IN (SELECT sp.product_id
                       FROM silver.products sp
                       JOIN gold.dim_products gdp ON sp.product_id = gdp.product_id
                       WHERE sp.product_price != gdp.product_price
                       AND gdp.is_current = FALSE);

-- I am leaving this update query to reconcile with our orders table generation
--UPDATE gold.dim_products SET valid_from = '2025-01-01' WHERE is_current = TRUE;