-- monthly revenues
select 
	d.year,
	d.month_name,
	SUM(f.total_price) as monthly_revenue,
	COUNT(distinct f.order_id) as total_orders
from gold.fact_orders f
join gold.dim_date d
on f.order_date = d.date_id
group by d.year, d.month_name, d.month
order by d.year, d.month;

-- top 5 products by revenue
SELECT
    gdp.product_name,
    SUM(f.total_price) AS total_revenue
FROM gold.fact_orders f
JOIN gold.dim_products gdp ON f.dim_product_key = gdp.dim_product_key
GROUP BY gdp.product_name
ORDER BY total_revenue DESC
LIMIT 5;