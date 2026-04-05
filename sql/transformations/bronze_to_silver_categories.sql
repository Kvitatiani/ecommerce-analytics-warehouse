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