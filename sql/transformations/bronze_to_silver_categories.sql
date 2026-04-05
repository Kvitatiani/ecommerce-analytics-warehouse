-- insert bronze raw categories into silver table
INSERT INTO silver.categories (category_id, category_name, category_slug, created_at, updated_at)
SELECT
    (categories_payload->>'id')::INTEGER AS category_id,
    categories_payload->>'name' AS category_name,
    categories_payload->>'slug' AS category_slug,
    (categories_payload->>'creationAt')::TIMESTAMP AS created_at,
    (categories_payload->>'updatedAt')::TIMESTAMP AS updated_at
FROM bronze.categories_raw
WHERE categories_payload->>'name' != ''
  AND categories_payload->>'name' ~ '^[A-Za-z\s\-]+$'
  AND categories_payload->>'slug' != ''
  AND (categories_payload->>'id')::INTEGER IS NOT NULL
  AND categories_payload IS NOT NULL
ON CONFLICT (category_id) DO UPDATE SET 
    category_name = EXCLUDED.category_name,
    category_slug = EXCLUDED.category_slug,
    created_at = EXCLUDED.created_at,
    updated_at = EXCLUDED.updated_at;


-- insert bronze raw users into silver table
INSERT INTO silver.customers (customer_id, customer_name, customer_email, customer_role, created_at, updated_at)
with ranked as (
	SELECT
	    (users_payload->>'id')::INTEGER AS customer_id,
	    users_payload->>'name' AS customer_name,
	    users_payload->>'email' AS customer_email,
	    users_payload->>'role' AS customer_role,
	    (users_payload->>'creationAt')::TIMESTAMP AS created_at,
	    (users_payload->>'updatedAt')::TIMESTAMP AS updated_at,
	    row_number() over (partition by users_payload->>'email' order by (users_payload->>'id')::INTEGER) as rn
	FROM bronze.users_raw
	WHERE users_payload->>'name' != ''
	    AND users_payload->>'email' != ''
	    AND users_payload->>'email' ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
	    AND users_payload->>'role' != ''
	    AND (users_payload->>'id')::INTEGER IS NOT NULL
	    AND users_payload IS NOT NULL
)
select
	customer_id,
    customer_name,
    customer_email,
    customer_role,
    created_at,
    updated_at
from ranked
where rn = 1
ON CONFLICT (customer_id) DO UPDATE SET
    customer_name = EXCLUDED.customer_name,
    customer_email = EXCLUDED.customer_email,
    customer_role = EXCLUDED.customer_role,
    created_at = EXCLUDED.created_at,
    updated_at = EXCLUDED.updated_at;

-- insert bronze raw products into silver
insert into silver.products (product_id, product_name, product_slug, product_price, product_description, product_category_id, created_at, updated_at)
SELECT
    (products_payload->>'id')::INTEGER AS product_id,
    products_payload->>'title' AS product_name,
    products_payload->>'slug' AS product_slug,
    (products_payload->>'price')::NUMERIC(10,2) AS product_price,
    products_payload->>'description' AS product_description,
    (products_payload->'category'->>'id')::INTEGER AS product_category_id,
    (products_payload->>'creationAt')::TIMESTAMP AS created_at,
    (products_payload->>'updatedAt')::TIMESTAMP AS updated_at
FROM bronze.products_raw
WHERE products_payload->>'title' != ''
  AND products_payload->>'slug' != ''
  AND (products_payload->>'price')::NUMERIC(10,2) >= 0
  AND (products_payload->'category'->>'id')::INTEGER IS NOT NULL
  AND (products_payload->'category'->>'id')::INTEGER IN (SELECT category_id FROM silver.categories)
  AND (products_payload->>'id')::INTEGER IS NOT NULL
  AND products_payload IS NOT NULL
ON CONFLICT (product_id) DO UPDATE SET
    product_name = EXCLUDED.product_name,
    product_slug = EXCLUDED.product_slug,
    product_price = EXCLUDED.product_price,
    product_description = EXCLUDED.product_description,
    product_category_id = EXCLUDED.product_category_id,
    created_at = EXCLUDED.created_at,
    updated_at = EXCLUDED.updated_at;