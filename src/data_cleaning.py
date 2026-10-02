import pandas as pd
from pathlib import Path

RAW = Path("data/raw/ecommerce_sales.csv")
OUT = Path("data/processed/cleaned_sales.csv")

def clean_data():
    df = pd.read_csv(RAW)

    # Standardize column names
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Correct data types
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    numeric_cols = [
        "age", "quantity", "unit_price", "discount_percent",
        "final_price", "cost_per_unit", "revenue", "cost", "profit"
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remove exact duplicates
    before = len(df)
    df = df.drop_duplicates()
    duplicates_removed = before - len(df)

    # Remove invalid dates and impossible quantities/prices
    df = df.dropna(subset=["order_id", "order_date", "customer_id"])
    df = df[df["quantity"] > 0]
    df = df[df["final_price"] >= 0]
    df = df[df["revenue"] >= 0]

    # Fill categorical missing values
    categorical = ["gender", "city", "state", "category", "product_name",
                    "payment_method", "order_status"]
    for col in categorical:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown").astype(str).str.strip()

    # Derived metrics
    df["profit_margin"] = (
        df["profit"].div(df["revenue"].replace(0, pd.NA)).mul(100)
    ).fillna(0).round(2)

    df["year"] = df["order_date"].dt.year
    df["month"] = df["order_date"].dt.month
    df["month_name"] = df["order_date"].dt.strftime("%b")
    df["year_month"] = df["order_date"].dt.to_period("M").astype(str)

    # Customer segment based on total customer revenue
    customer_revenue = df.groupby("customer_id")["revenue"].sum()
    q1, q2 = customer_revenue.quantile([0.33, 0.66])

    def segment(value):
        if value <= q1:
            return "Low Value"
        elif value <= q2:
            return "Medium Value"
        return "High Value"

    df["customer_segment"] = df["customer_id"].map(customer_revenue).map(segment)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)

    print(f"Rows before cleaning: {before:,}")
    print(f"Duplicates removed: {duplicates_removed:,}")
    print(f"Rows after cleaning: {len(df):,}")
    print(f"Saved: {OUT}")

if __name__ == "__main__":
    clean_data()
