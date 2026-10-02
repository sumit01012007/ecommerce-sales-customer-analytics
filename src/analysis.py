import pandas as pd
from pathlib import Path

INPUT = Path("data/processed/cleaned_sales.csv")
OUT = Path("outputs")
OUT.mkdir(exist_ok=True)

df = pd.read_csv(INPUT, parse_dates=["order_date"])

delivered = df[df["order_status"] == "Delivered"].copy()

total_revenue = delivered["revenue"].sum()
total_profit = delivered["profit"].sum()
total_orders = delivered["order_id"].nunique()
total_customers = delivered["customer_id"].nunique()
aov = total_revenue / total_orders if total_orders else 0
margin = total_profit / total_revenue * 100 if total_revenue else 0

summary = pd.DataFrame({
    "Metric": [
        "Total Revenue", "Total Profit", "Total Orders",
        "Total Customers", "Average Order Value", "Profit Margin %"
    ],
    "Value": [
        total_revenue, total_profit, total_orders,
        total_customers, aov, margin
    ]
})
summary.to_csv(OUT / "kpi_summary.csv", index=False)

monthly = delivered.groupby("year_month").agg(
    Revenue=("revenue", "sum"),
    Profit=("profit", "sum"),
    Orders=("order_id", "nunique")
).reset_index()
monthly.to_csv(OUT / "monthly_sales.csv", index=False)

category = delivered.groupby("category").agg(
    Revenue=("revenue", "sum"),
    Profit=("profit", "sum"),
    Quantity=("quantity", "sum"),
    Orders=("order_id", "nunique")
).sort_values("Revenue", ascending=False).reset_index()
category.to_csv(OUT / "category_performance.csv", index=False)

products = delivered.groupby("product_name").agg(
    Revenue=("revenue", "sum"),
    Profit=("profit", "sum"),
    Quantity=("quantity", "sum")
).sort_values("Revenue", ascending=False).reset_index()
products.to_csv(OUT / "product_performance.csv", index=False)

regions = delivered.groupby(["state", "city"]).agg(
    Revenue=("revenue", "sum"),
    Profit=("profit", "sum"),
    Orders=("order_id", "nunique")
).sort_values("Revenue", ascending=False).reset_index()
regions.to_csv(OUT / "regional_performance.csv", index=False)

customers = delivered.groupby("customer_id").agg(
    Revenue=("revenue", "sum"),
    Orders=("order_id", "nunique"),
    Quantity=("quantity", "sum")
).sort_values("Revenue", ascending=False).reset_index()
customers["Average_Order_Value"] = customers["Revenue"] / customers["Orders"]
customers.to_csv(OUT / "customer_performance.csv", index=False)

print("\nKEY PERFORMANCE INDICATORS")
print("-" * 40)
for _, row in summary.iterrows():
    print(f"{row['Metric']}: {row['Value']:,.2f}")
