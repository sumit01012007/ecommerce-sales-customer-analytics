# E-Commerce Sales & Customer Analytics

An end-to-end Data Analyst internship project built with Python, Pandas, SQL, and Power BI.

## Tech Stack
- Python
- Pandas
- NumPy
- Matplotlib
- SQL / SQLite
- Scikit-learn
- Power BI
- VS Code
- Git & GitHub

## Project Pipeline

Raw CSV
→ Data Cleaning
→ Feature Engineering
→ Exploratory Data Analysis
→ SQL Business Analysis
→ Customer Segmentation
→ Power BI Dashboard
→ Business Insights

## Folder Structure

```text
ecommerce-data-analytics/
├── data/
│   ├── raw/
│   │   └── ecommerce_sales.csv
│   └── processed/
├── notebooks/
├── sql/
├── src/
├── outputs/
├── reports/
├── dashboard/
├── requirements.txt
├── README.md
└── .gitignore
```

## Setup

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install packages:

```bash
pip install -r requirements.txt
```

Run cleaning:

```bash
python src/data_cleaning.py
```

Run analysis:

```bash
python src/analysis.py
```

Generate charts:

```bash
python src/visualization.py
```

## Power BI

Import:
`data/processed/cleaned_sales.csv`

Recommended pages:
1. Executive Overview
2. Product & Category Analysis
3. Customer Analysis
4. Regional Analysis

## Dashboard KPIs
- Total Revenue
- Total Profit
- Total Orders
- Total Customers
- Average Order Value
- Profit Margin
- Return/Cancel Rate

## Disclaimer
The dataset is synthetic and created for educational, portfolio, and internship demonstration purposes.
