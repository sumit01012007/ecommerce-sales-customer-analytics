import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

df = pd.read_csv("data/processed/cleaned_sales.csv", parse_dates=["order_date"])
df = df[df["order_status"] == "Delivered"].copy()
out = Path("outputs")
out.mkdir(exist_ok=True)

# Monthly revenue
monthly = df.groupby("year_month")["revenue"].sum()
plt.figure(figsize=(12, 5))
monthly.plot(marker="o")
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(out / "monthly_revenue.png", dpi=150)
plt.close()

# Category revenue
category = df.groupby("category")["revenue"].sum().sort_values()
plt.figure(figsize=(9, 5))
category.plot(kind="barh")
plt.title("Revenue by Category")
plt.xlabel("Revenue")
plt.tight_layout()
plt.savefig(out / "category_revenue.png", dpi=150)
plt.close()

# Top products
top = df.groupby("product_name")["revenue"].sum().nlargest(10).sort_values()
plt.figure(figsize=(10, 6))
top.plot(kind="barh")
plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue")
plt.tight_layout()
plt.savefig(out / "top_10_products.png", dpi=150)
plt.close()

# Regional revenue
region = df.groupby("state")["revenue"].sum().nlargest(10).sort_values()
plt.figure(figsize=(10, 6))
region.plot(kind="barh")
plt.title("Top 10 States by Revenue")
plt.xlabel("Revenue")
plt.tight_layout()
plt.savefig(out / "top_states.png", dpi=150)
plt.close()

# Customer segments
segments = df.groupby("customer_segment")["revenue"].sum()
plt.figure(figsize=(7, 5))
segments.plot(kind="pie", autopct="%1.1f%%")
plt.title("Revenue by Customer Segment")
plt.ylabel("")
plt.tight_layout()
plt.savefig(out / "customer_segments.png", dpi=150)
plt.close()

print("Charts generated in outputs/")
