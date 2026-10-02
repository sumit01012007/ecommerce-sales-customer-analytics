-- 1. Total revenue
SELECT ROUND(SUM(revenue), 2) AS total_revenue
FROM sales
WHERE order_status = 'Delivered';

-- 2. Total profit
SELECT ROUND(SUM(profit), 2) AS total_profit
FROM sales
WHERE order_status = 'Delivered';

-- 3. Monthly revenue
SELECT year_month,
       ROUND(SUM(revenue), 2) AS revenue
FROM sales
WHERE order_status = 'Delivered'
GROUP BY year_month
ORDER BY year_month;

-- 4. Category performance
SELECT category,
       ROUND(SUM(revenue), 2) AS revenue,
       ROUND(SUM(profit), 2) AS profit
FROM sales
WHERE order_status = 'Delivered'
GROUP BY category
ORDER BY revenue DESC;

-- 5. Top 10 products
SELECT product_name,
       ROUND(SUM(revenue), 2) AS revenue
FROM sales
WHERE order_status = 'Delivered'
GROUP BY product_name
ORDER BY revenue DESC
LIMIT 10;

-- 6. Bottom 10 products
SELECT product_name,
       ROUND(SUM(revenue), 2) AS revenue
FROM sales
WHERE order_status = 'Delivered'
GROUP BY product_name
ORDER BY revenue ASC
LIMIT 10;

-- 7. Revenue by state
SELECT state,
       ROUND(SUM(revenue), 2) AS revenue,
       ROUND(SUM(profit), 2) AS profit
FROM sales
WHERE order_status = 'Delivered'
GROUP BY state
ORDER BY revenue DESC;

-- 8. Payment method analysis
SELECT payment_method,
       COUNT(*) AS transactions,
       ROUND(SUM(revenue), 2) AS revenue
FROM sales
WHERE order_status = 'Delivered'
GROUP BY payment_method
ORDER BY revenue DESC;

-- 9. Customer segment analysis
SELECT customer_segment,
       COUNT(DISTINCT customer_id) AS customers,
       ROUND(SUM(revenue), 2) AS revenue
FROM sales
WHERE order_status = 'Delivered'
GROUP BY customer_segment
ORDER BY revenue DESC;

-- 10. Average order value
SELECT ROUND(
    SUM(revenue) / COUNT(DISTINCT order_id), 2
) AS average_order_value
FROM sales
WHERE order_status = 'Delivered';

-- 11. Return/cancellation rate
SELECT order_status,
       COUNT(*) AS orders,
       ROUND(
           COUNT(*) * 100.0 / (SELECT COUNT(*) FROM sales), 2
       ) AS percentage
FROM sales
GROUP BY order_status;

-- 12. Gender analysis
SELECT gender,
       COUNT(DISTINCT customer_id) AS customers,
       ROUND(SUM(revenue), 2) AS revenue
FROM sales
WHERE order_status = 'Delivered'
GROUP BY gender;

-- 13. Age group analysis
SELECT
    CASE
        WHEN age < 25 THEN '18-24'
        WHEN age < 35 THEN '25-34'
        WHEN age < 45 THEN '35-44'
        WHEN age < 55 THEN '45-54'
        ELSE '55+'
    END AS age_group,
    ROUND(SUM(revenue), 2) AS revenue
FROM sales
WHERE order_status = 'Delivered'
GROUP BY age_group
ORDER BY revenue DESC;

-- 14. High-value customers
SELECT customer_id,
       ROUND(SUM(revenue), 2) AS revenue,
       COUNT(DISTINCT order_id) AS orders
FROM sales
WHERE order_status = 'Delivered'
GROUP BY customer_id
HAVING SUM(revenue) > 10000
ORDER BY revenue DESC;

-- 15. Profit margin by category
SELECT category,
       ROUND(SUM(profit) * 100.0 / SUM(revenue), 2) AS profit_margin
FROM sales
WHERE order_status = 'Delivered'
GROUP BY category
ORDER BY profit_margin DESC;
