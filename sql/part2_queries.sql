-- Q1: Total revenue per city (top 10)
SELECT c.city, SUM(o.total_amount) AS total_revenue
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.city
ORDER BY total_revenue DESC
LIMIT 10;

-- Q2: Top 5 customers by number of orders
SELECT c.customer_name, COUNT(o.order_id) AS order_count
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_name
ORDER BY order_count DESC
LIMIT 5;

-- Q3: Average order value per month
SELECT DATE_TRUNC('month', order_date) AS month,
       AVG(total_amount) AS avg_order_value
FROM orders
GROUP BY month
ORDER BY month;

-- Q4: Customers with more than 10 orders
SELECT c.customer_name, COUNT(*) AS num_orders
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_name
HAVING COUNT(*) > 10
ORDER BY num_orders DESC;

-- Q5: Orders with total_amount above average (Subquery)
SELECT order_id, product, total_amount
FROM orders
WHERE total_amount > (SELECT AVG(total_amount) FROM orders)
ORDER BY total_amount DESC
LIMIT 20;

-- Q6: Revenue by payment method and status
SELECT payment_method, status, 
       SUM(total_amount) AS revenue,
       COUNT(*) AS num_orders
FROM orders
GROUP BY payment_method, status
ORDER BY payment_method, status;

-- Q7: Create a VIEW for city revenue summary
CREATE VIEW city_revenue_summary AS
SELECT c.city, 
       COUNT(o.order_id) AS total_orders,
       SUM(o.total_amount) AS total_revenue,
       AVG(o.total_amount) AS avg_order_value
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.city;

-- Test the view
SELECT * FROM city_revenue_summary ORDER BY total_revenue DESC;

-- Q8: Create an INDEX on frequently filtered columns
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_customer ON orders(customer_id);

-- Test: this query should be faster now
EXPLAIN ANALYZE
SELECT * FROM orders WHERE order_date >= '2026-06-01' AND status = 'Delivered';