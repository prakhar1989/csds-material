/* Solutions for the Hive Assignment: */

/* 1. What is the average price of the products that were purchased via Mastercard? */

SELECT AVG(price) 
FROM purchases 
WHERE card=”MasterCard”;

> 275.0677

/* 2. Which date recorded the highest total sales?

- need to group by according to to_date(sales_date) and not just sales_date because the field contains time information also.
*/

SELECT to_date(sales_date), SUM(price) AS total_sales 
FROM purchases 
GROUP BY to_date(sales_date) 
SORT BY total_sales DESC LIMIT 1;

> 2012-03-17  2384.48

/* 3. What is the minimum value of a product under the Computers category? */

SELECT MIN(price) 
FROM purchases 
WHERE category=”Computers”;

> 0.38

/* 4. How many distinct categories of products are there? */

SELECT COUNT(DISTINCT category) 
FROM purchases;

> 18

/* 5. Which store location had the lowest total sales? */

SELECT store_location, SUM(price) AS store_sales 
FROM purchases 
GROUP BY store_location 
ORDER BY store_sales LIMIT 1;

> Plano 784.9599

