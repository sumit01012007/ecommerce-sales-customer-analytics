# Power BI Dashboard Guide

## Import
Get Data -> Text/CSV -> data/processed/cleaned_sales.csv

## Measures
Total Revenue = SUM(sales[revenue])
Total Profit = SUM(sales[profit])
Total Orders = DISTINCTCOUNT(sales[order_id])
Total Customers = DISTINCTCOUNT(sales[customer_id])
Average Order Value = DIVIDE([Total Revenue], [Total Orders])
Profit Margin % = DIVIDE([Total Profit], [Total Revenue])

## Page 1: Executive Overview
Cards: Revenue, Profit, Orders, Customers, AOV, Profit Margin
Charts: monthly revenue line chart, category revenue bar chart

## Page 2: Product Analysis
Top 10 products, category revenue/profit, quantity sold

## Page 3: Customer Analysis
Customer segments, gender, age groups, top customers

## Page 4: Regional Analysis
State revenue, state profit, city performance, payment methods

## Recommended slicers
Year, Month, State, Category, Payment Method, Order Status
