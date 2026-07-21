SELECT *
FROM dim_customer;

SELECT *
FROM dim_date;

SELECT *
FROM dim_location;

SELECT *
FROM dim_product;

SELECT *
FROM dim_ship_mode;

SELECT *
FROM fact_sales;

-- 1: Total Sales
SELECT SUM(sales) AS total_sales
FROM fact_sales;
-- 2: Total Profit
SELECT SUM(profit) AS total_profit
FROM fact_sales;
-- 3: Total Orders
SELECT COUNT(order_id) AS total_orders
FROM fact_sales;
-- 4: Average Sales
SELECT ROUND(AVG(sales),2) AS average_sales
FROM fact_sales;
--5: Average Profit
SELECT ROUND(AVG(profit),2) AS average_profit
FROM fact_sales;

--6: Sales by Year
SELECT 
	dd.order_year,
	sum(fs.sales) AS sales
FROM fact_sales fs
JOIN dim_date dd
ON fs.date_id=dd.date_id
GROUP BY dd.order_year
ORDER BY dd.order_year;
--7: Profit by year
SELECT  
	dd.order_year,
	SUM(fs.profit) AS profit
FROM fact_sales fs
JOIN dim_date dd
ON fs.date_id = dd.date_id
GROUP BY dd.order_year
ORDER BY dd.order_year;
--8: Sales by Quarter
SELECT
	dd.order_year,
	dd.quarter,
	sum(fs.sales) AS sales
FROM fact_sales fs
JOIN dim_date dd
ON fs.date_id=dd.date_id
GROUP BY 
	dd.order_year,
	dd.quarter
ORDER BY 
	dd.order_year,
	dd.quarter;
--9: Monthly Trend Analysis
SELECT
    dd.order_year,
    dd.order_month,
    SUM(fs.sales) AS total_sales
FROM fact_sales fs
JOIN dim_date dd
ON fs.date_id = dd.date_id
GROUP BY
    dd.order_year,
    dd.month_number,
    dd.order_month
ORDER BY
    dd.order_year,
    dd.month_number;

--10: Top 10 Customers by Sales
SELECT
	dc.customer_id,
	dc.customer_name,
	SUM(fs.sales) AS sales
FROM fact_sales fs
JOIN dim_customer dc
ON fs.customer_id = dc.customer_id
GROUP BY
	dc.customer_id,
	dc.customer_name
ORDER BY sales DESC
LIMIT 10;

--11:Top 10 Products by Profit
SELECT 
	dp.product_name,
	SUM(fs.profit) AS total_profit
FROM fact_sales fs
JOIN dim_product dp
ON fs.product_id = dp.product_id
GROUP BY dp.product_name
ORDER BY total_profit DESC
LIMIT 10;

--12:Most Profitable Categories
SELECT
	dp.category,
	SUM(fs.profit) AS total_profit
FROM fact_sales fs
JOIN dim_product dp
ON fs.product_id = dp.product_id
GROUP BY dp.category
ORDER BY total_profit DESC;

--13:Top Performing Region
SELECT 
	dl.region,
	SUM(fs.sales) AS total_sales
FROM fact_sales fs
JOIN dim_location dl
ON fs.location_id = dl.location_id
GROUP BY dl.region
ORDER BY total_sales DESC
LIMIT 1;

--14:Bottom 10 Loss-Making Products
SELECT
    dp.product_name,
    ROUND(SUM(fs.profit), 2) AS total_profit
FROM fact_sales fs
JOIN dim_product dp
ON fs.product_id = dp.product_id
GROUP BY dp.product_name
ORDER BY total_profit ASC
LIMIT 10;

--15:Customer Ranking
SELECT
	dc.customer_name,
	SUM(fs.sales) AS total_sales,
	DENSE_RANK()
	OVER(ORDER BY SUM(fs.sales) DESC) AS customer_rank
FROM fact_sales fs
join dim_customer dc
ON fs.customer_id = dc.customer_id
GROUP BY dc.customer_name;

--16:Product Ranking
SELECT 
	dp.product_name,
	SUM(fs.sales) AS total_sales,
	DENSE_RANK()
	OVER(ORDER BY SUM(fs.sales) DESC) AS product_rank
FROM fact_sales fs
join dim_product dp
ON fs.product_id = dp.product_id
GROUP BY dp.product_name;

--17:Year-over-Year (YoY) Sales Growth
WITH yearly_sales AS (
    SELECT
        dd.order_year,
        ROUND(SUM(fs.sales), 2) AS total_sales
    FROM fact_sales fs
    JOIN dim_date dd
        ON fs.date_id = dd.date_id
    GROUP BY dd.order_year
	ORDER BY dd.order_year
)
SELECT 
	order_year,
	total_sales,
	LAG(total_sales)
		OVER(ORDER BY order_year) AS previous_year_sales
FROM yearly_sales;

--18: Sales Growth Amount
WITH yearly_sales AS (
    SELECT
        dd.order_year,
        ROUND(SUM(fs.sales), 2) AS total_sales
    FROM fact_sales fs
    JOIN dim_date dd
        ON fs.date_id = dd.date_id
    GROUP BY dd.order_year
	),
sales_comparison AS (
    SELECT
        order_year,
        total_sales,
        LAG(total_sales) OVER (ORDER BY order_year) AS previous_year_sales
    FROM yearly_sales
)

SELECT
    order_year,
    total_sales,
    previous_year_sales,
    ROUND(total_sales - previous_year_sales, 2) AS sales_growth
FROM sales_comparison
ORDER BY order_year;

--19:Year-over-Year (YoY) Growth %
WITH yearly_sales AS (
    SELECT
        dd.order_year,
        ROUND(SUM(fs.sales), 2) AS total_sales
    FROM fact_sales fs
    JOIN dim_date dd
        ON fs.date_id = dd.date_id
    GROUP BY dd.order_year
),

sales_comparison AS (
    SELECT
        order_year,
        total_sales,
        LAG(total_sales) OVER (ORDER BY order_year) AS previous_year_sales
    FROM yearly_sales
)

SELECT
    order_year,
    total_sales,
    previous_year_sales,
    ROUND(total_sales - previous_year_sales, 2) AS sales_growth,
    ROUND(
        ((total_sales - previous_year_sales) / previous_year_sales) * 100,
        2
    ) AS yoy_growth_percentage
FROM sales_comparison
ORDER BY order_year;

--20:Month-over-Month (MoM) Growth
WITH monthly_sales AS (
    SELECT
        dd.order_year,
        dd.month_number,
        dd.order_month,
        ROUND(SUM(fs.sales), 2) AS total_sales
    FROM fact_sales fs
    JOIN dim_date dd
        ON fs.date_id = dd.date_id
    GROUP BY
        dd.order_year,
        dd.month_number,
        dd.order_month
)
SELECT *
FROM monthly_sales
ORDER BY
    order_year,
    month_number;

--21:Month-over-Month (MoM) Sales Growth
WITH monthly_sales AS (
    SELECT
        dd.order_year,
        dd.month_number,
        dd.order_month,
        ROUND(SUM(fs.sales),2) AS total_sales
    FROM fact_sales fs
    JOIN dim_date dd
        ON fs.date_id = dd.date_id
    GROUP BY
        dd.order_year,
        dd.month_number,
        dd.order_month
),
monthly_comparison AS (
    SELECT
        order_year,
        month_number,
        order_month,
        total_sales,
        LAG(total_sales)
        OVER(ORDER BY order_year, month_number) AS previous_month_sales
    FROM monthly_sales
)
SELECT
    order_year,
    order_month,
    total_sales,
    previous_month_sales,
    ROUND(total_sales - previous_month_sales,2) AS sales_growth,
    ROUND(
        ((total_sales - previous_month_sales)
        / NULLIF(previous_month_sales,0))*100,
        2
    ) AS mom_growth_percentage
FROM monthly_comparison
ORDER BY order_year, month_number;

--22:Running Total (Cumulative Sales)
WITH monthly_sales AS (
    SELECT
        dd.order_year,
        dd.month_number,
        dd.order_month,
        ROUND(SUM(fs.sales),2) AS total_sales
    FROM fact_sales fs
    JOIN dim_date dd
        ON fs.date_id = dd.date_id
    GROUP BY
        dd.order_year,
        dd.month_number,
        dd.order_month
)

SELECT
    order_year,
    order_month,
    total_sales,
    ROUND(
        SUM(total_sales)
        OVER(
            ORDER BY order_year, month_number
        ),
        2
    ) AS running_total_sales
FROM monthly_sales
ORDER BY order_year, month_number;

--23:Percentage Contribution by Region
SELECT
    dl.region,
    ROUND(SUM(fs.sales),2) AS total_sales,
    ROUND(
        SUM(fs.sales)
        *100.0/
        SUM(SUM(fs.sales)) OVER(),
        2
    ) AS contribution_percentage
FROM fact_sales fs
JOIN dim_location dl
ON fs.location_id = dl.location_id
GROUP BY dl.region
ORDER BY total_sales DESC;

--24:Category-wise Sales Contribution
SELECT
    dp.category,
    ROUND(SUM(fs.sales),2) AS total_sales,
    ROUND(
        SUM(fs.sales)
        *100.0/
        SUM(SUM(fs.sales)) OVER(),
        2
    ) AS contribution_percentage
FROM fact_sales fs
JOIN dim_product dp
ON fs.product_id = dp.product_id
GROUP BY dp.category
ORDER BY total_sales DESC;

--25: Top Customer in Each Region
WITH customer_sales AS (
SELECT
dl.region,
dc.customer_name,
ROUND(SUM(fs.sales),2) AS total_sales
FROM fact_sales fs
JOIN dim_customer dc
ON fs.customer_id=dc.customer_id
JOIN dim_location dl
ON fs.location_id=dl.location_id
GROUP BY
dl.region,
dc.customer_name
)
SELECT *
FROM(
SELECT
*,
ROW_NUMBER()
OVER(
PARTITION BY region
ORDER BY total_sales DESC
) AS rank
FROM customer_sales
)t
WHERE rank=1;

--26:Best Product in Each Category
WITH product_sales AS (

SELECT

dp.category,

dp.product_name,

ROUND(SUM(fs.sales),2) AS total_sales

FROM fact_sales fs

JOIN dim_product dp

ON fs.product_id=dp.product_id

GROUP BY
dp.category,
dp.product_name

)

SELECT *

FROM(

SELECT

*,

ROW_NUMBER()

OVER(
PARTITION BY category
ORDER BY total_sales DESC
) AS rank

FROM product_sales

)t

WHERE rank=1;

--27:Top 5 Products in Each Category
WITH product_sales AS (

SELECT

dp.category,

dp.product_name,

ROUND(SUM(fs.sales),2) AS total_sales

FROM fact_sales fs

JOIN dim_product dp

ON fs.product_id=dp.product_id

GROUP BY
dp.category,
dp.product_name

)

SELECT *

FROM(

SELECT

*,

DENSE_RANK()

OVER(
PARTITION BY category
ORDER BY total_sales DESC
) AS product_rank

FROM product_sales

)t

WHERE product_rank<=5;

--28:Running Profit
WITH monthly_profit AS (

SELECT

dd.order_year,

dd.month_number,

dd.order_month,

ROUND(SUM(fs.profit),2) AS total_profit

FROM fact_sales fs

JOIN dim_date dd

ON fs.date_id=dd.date_id

GROUP BY
dd.order_year,
dd.month_number,
dd.order_month

)

SELECT

order_year,

order_month,

total_profit,

ROUND(

SUM(total_profit)

OVER(

ORDER BY order_year,month_number

),2

) AS running_profit

FROM monthly_profit

ORDER BY order_year,month_number;

--29:Highest Profit Month
SELECT

dd.order_year,

dd.order_month,

ROUND(SUM(fs.profit),2) AS total_profit

FROM fact_sales fs

JOIN dim_date dd

ON fs.date_id=dd.date_id

GROUP BY
dd.order_year,
dd.month_number,
dd.order_month

ORDER BY total_profit DESC

LIMIT 1;

--30:Lowest Profit Month
SELECT

dd.order_year,

dd.order_month,

ROUND(SUM(fs.profit),2) AS total_profit

FROM fact_sales fs

JOIN dim_date dd

ON fs.date_id=dd.date_id

GROUP BY
dd.order_year,
dd.month_number,
dd.order_month

ORDER BY total_profit

LIMIT 1;

