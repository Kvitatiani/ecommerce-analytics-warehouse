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