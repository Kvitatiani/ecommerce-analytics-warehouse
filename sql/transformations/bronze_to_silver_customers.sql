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