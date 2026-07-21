CREATE TABLE dim_customer (
    customer_id TEXT PRIMARY KEY,
    customer_name TEXT NOT NULL,
    segment TEXT NOT NULL
);

select * from dim_customer;

CREATE TABLE dim_product (
    product_id TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    sub_category TEXT NOT NULL
);

SELECT *
FROM dim_product ;

CREATE TABLE dim_location (
    location_id SERIAL PRIMARY KEY,
    postal_code INTEGER NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    region TEXT NOT NULL,
    country TEXT NOT NULL
);

CREATE TABLE dim_ship_mode (
    ship_mode_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    ship_mode TEXT NOT NULL
);

CREATE TABLE dim_date (
    date_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_date DATE NOT NULL,
    order_year INTEGER NOT NULL,
    order_month TEXT NOT NULL,
    month_number INTEGER NOT NULL,
    quarter TEXT NOT NULL,
    day_name TEXT NOT NULL
);

CREATE TABLE fact_sales (
    sale_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id TEXT NOT NULL,
    customer_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    location_id INTEGER NOT NULL,
    ship_mode_id INTEGER NOT NULL,
    date_id INTEGER NOT NULL,
    sales NUMERIC(10,2) NOT NULL,
    quantity INTEGER NOT NULL,
    discount NUMERIC(4,2) NOT NULL,
    profit NUMERIC(10,2) NOT NULL,
    shipping_days INTEGER NOT NULL,
    profit_margin NUMERIC(5,2) NOT NULL,
    loss_order BOOLEAN NOT NULL,
CONSTRAINT fk_customer
        FOREIGN KEY (customer_id)
        REFERENCES dim_customer(customer_id),
    CONSTRAINT fk_product
        FOREIGN KEY (product_id)
        REFERENCES dim_product(product_id),
    CONSTRAINT fk_location
        FOREIGN KEY (location_id)
        REFERENCES dim_location(location_id),
    CONSTRAINT fk_ship_mode
        FOREIGN KEY (ship_mode_id)
        REFERENCES dim_ship_mode(ship_mode_id),
    CONSTRAINT fk_date
        FOREIGN KEY (date_id)
        REFERENCES dim_date(date_id)
);
----------------------------------
SELECT * FROM dim_customer;

SELECT COUNT(*)
FROM dim_customer;

SELECT COUNT(*)
FROM dim_product;

SELECT COUNT(*)
FROM dim_location;

SELECT COUNT(*)
FROM dim_ship_mode;

SELECT COUNT(*)
FROM dim_date;

SELECT COUNT(*)
FROM fact_sales;

SELECT COUNT(*) AS total_sales
FROM fact_sales;

SELECT *
FROM fact_sales
WHERE customer_id IS NULL
   OR product_id IS NULL
   OR location_id IS NULL
   OR ship_mode_id IS NULL
   OR date_id IS NULL;

SELECT
    c.customer_name,
    p.product_name,
    d.order_year,
    f.sales,
    f.profit
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_id = c.customer_id
JOIN dim_product p
    ON f.product_id = p.product_id
JOIN dim_date d
    ON f.date_id = d.date_id
LIMIT 10;



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