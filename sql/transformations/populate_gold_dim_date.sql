INSERT INTO gold.dim_date (date_id, year, quarter, month, day, day_of_week, is_weekend, month_name, day_name)
SELECT
    date_id,
    EXTRACT(YEAR FROM date_id) AS year,
    EXTRACT(QUARTER FROM date_id) AS quarter,
    EXTRACT(MONTH FROM date_id) AS month,
    EXTRACT(DAY FROM date_id) AS day,
    EXTRACT(DOW FROM date_id) AS day_of_week,
    CASE WHEN EXTRACT(DOW FROM date_id) IN (0, 6) THEN TRUE ELSE FALSE END AS is_weekend,
    TO_CHAR(date_id, 'Month') AS month_name,
    TO_CHAR(date_id, 'Day') AS day_name
FROM (
    SELECT generate_series('2025-10-01'::DATE, '2030-12-31'::DATE, '1 day') AS date_id
) AS date_series
ON CONFLICT (date_id) DO UPDATE SET
    year = EXCLUDED.year,
    quarter = EXCLUDED.quarter,
    month = EXCLUDED.month,
    day = EXCLUDED.day,
    day_of_week = EXCLUDED.day_of_week,
    is_weekend = EXCLUDED.is_weekend,
    month_name = EXCLUDED.month_name,
    day_name = EXCLUDED.day_name;