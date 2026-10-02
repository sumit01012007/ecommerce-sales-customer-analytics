import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="E-Commerce Sales Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #f7f8fc;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

/* Header */
.dashboard-title {
    font-size: 38px;
    font-weight: 750;
    margin-bottom: 0px;
}

.dashboard-subtitle {
    color: #6b7280;
    font-size: 16px;
    margin-bottom: 25px;
}

/* KPI cards */
.kpi-card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    min-height: 130px;
}

.kpi-title {
    color: #6b7280;
    font-size: 14px;
    font-weight: 600;
}

.kpi-value {
    font-size: 28px;
    font-weight: 750;
    margin-top: 8px;
}

.kpi-description {
    color: #6b7280;
    font-size: 12px;
    margin-top: 5px;
}

/* Section titles */
.section-title {
    font-size: 22px;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 10px;
}

/* Insight box */
.insight-box {
    background: white;
    border-left: 5px solid #6366f1;
    padding: 15px 18px;
    border-radius: 10px;
    margin-bottom: 10px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.03);
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

DATA_PATH = Path("data/processed/cleaned_sales.csv")

if not DATA_PATH.exists():
    st.error(
        "cleaned_sales.csv was not found. "
        "Run the following command first:\n\n"
        "python src/data_cleaning.py"
    )
    st.stop()

df = pd.read_csv(DATA_PATH)

df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🎛️ Dashboard Filters")
st.sidebar.markdown("---")

# Status
status_options = sorted(df["order_status"].dropna().unique())

selected_status = st.sidebar.multiselect(
    "Order Status",
    status_options,
    default=["Delivered"] if "Delivered" in status_options else status_options
)

# Category
category_options = sorted(df["category"].dropna().unique())

selected_categories = st.sidebar.multiselect(
    "Category",
    category_options,
    default=category_options
)

# State
state_options = sorted(df["state"].dropna().unique())

selected_states = st.sidebar.multiselect(
    "State",
    state_options,
    default=state_options
)

# Gender
gender_options = sorted(df["gender"].dropna().unique())

selected_gender = st.sidebar.multiselect(
    "Gender",
    gender_options,
    default=gender_options
)

# Date range
min_date = df["order_date"].min().date()
max_date = df["order_date"].max().date()

date_range = st.sidebar.date_input(
    "Order Date",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

st.sidebar.markdown("---")

st.sidebar.info(
    "📌 Use the filters to dynamically explore sales, "
    "customers, products and regional performance."
)


# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df.copy()

if selected_status:
    filtered_df = filtered_df[
        filtered_df["order_status"].isin(selected_status)
    ]

if selected_categories:
    filtered_df = filtered_df[
        filtered_df["category"].isin(selected_categories)
    ]

if selected_states:
    filtered_df = filtered_df[
        filtered_df["state"].isin(selected_states)
    ]

if selected_gender:
    filtered_df = filtered_df[
        filtered_df["gender"].isin(selected_gender)
    ]

if len(date_range) == 2:

    start_date = pd.Timestamp(date_range[0])
    end_date = pd.Timestamp(date_range[1]) + pd.Timedelta(days=1)

    filtered_df = filtered_df[
        (filtered_df["order_date"] >= start_date)
        & (filtered_df["order_date"] < end_date)
    ]


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="dashboard-title">📊 E-Commerce Sales Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Interactive business intelligence dashboard for sales, customers, '
    'products and regional performance'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# NO DATA CHECK
# =========================================================

if filtered_df.empty:

    st.warning(
        "No records match the selected filters. "
        "Please change your filters."
    )

    st.stop()


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_revenue = filtered_df["revenue"].sum()
total_profit = filtered_df["profit"].sum()

total_orders = filtered_df["order_id"].nunique()
total_customers = filtered_df["customer_id"].nunique()

total_quantity = filtered_df["quantity"].sum()

average_order_value = (
    total_revenue / total_orders
    if total_orders > 0
    else 0
)

profit_margin = (
    total_profit / total_revenue * 100
    if total_revenue > 0
    else 0
)


# =========================================================
# KPI CARDS
# =========================================================

k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">💰 TOTAL REVENUE</div>
            <div class="kpi-value">₹{total_revenue:,.0f}</div>
            <div class="kpi-description">Gross sales generated</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">📈 TOTAL PROFIT</div>
            <div class="kpi-value">₹{total_profit:,.0f}</div>
            <div class="kpi-description">{profit_margin:.2f}% profit margin</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">🛒 TOTAL ORDERS</div>
            <div class="kpi-value">{total_orders:,}</div>
            <div class="kpi-description">Unique orders</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">👥 CUSTOMERS</div>
            <div class="kpi-value">{total_customers:,}</div>
            <div class="kpi-description">Unique customers</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k5:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">🧾 AVG ORDER VALUE</div>
            <div class="kpi-value">₹{average_order_value:,.0f}</div>
            <div class="kpi-description">{total_quantity:,} units sold</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Sales Overview",
    "📦 Product Analysis",
    "👥 Customer Analysis",
    "🌎 Regional Analysis",
    "💡 Business Insights"
])


# =========================================================
# TAB 1 - SALES OVERVIEW
# =========================================================

with tab1:

    st.markdown(
        '<div class="section-title">Sales Performance</div>',
        unsafe_allow_html=True
    )

    monthly = (
        filtered_df
        .assign(year_month=filtered_df["order_date"].dt.to_period("M").astype(str))
        .groupby("year_month", as_index=False)
        .agg(
            Revenue=("revenue", "sum"),
            Profit=("profit", "sum"),
            Orders=("order_id", "nunique")
        )
    )

    col1, col2 = st.columns(2)

    with col1:

        fig = px.line(
            monthly,
            x="year_month",
            y="Revenue",
            markers=True,
            title="Monthly Revenue Trend",
            labels={
                "year_month": "Month",
                "Revenue": "Revenue (₹)"
            }
        )

        fig.update_layout(
            height=420,
            hovermode="x unified"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.line(
            monthly,
            x="year_month",
            y="Profit",
            markers=True,
            title="Monthly Profit Trend",
            labels={
                "year_month": "Month",
                "Profit": "Profit (₹)"
            }
        )

        fig.update_layout(
            height=420,
            hovermode="x unified"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # Category
    category = (
        filtered_df
        .groupby("category", as_index=False)
        .agg(
            Revenue=("revenue", "sum"),
            Profit=("profit", "sum"),
            Orders=("order_id", "nunique")
        )
        .sort_values("Revenue", ascending=False)
    )

    st.markdown(
        '<div class="section-title">Category Performance</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            category,
            x="category",
            y="Revenue",
            title="Revenue by Category",
            text_auto=".2s"
        )

        fig.update_layout(height=400)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.pie(
            category,
            names="category",
            values="Revenue",
            title="Revenue Distribution"
        )

        fig.update_layout(height=400)

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# TAB 2 - PRODUCT ANALYSIS
# =========================================================

with tab2:

    st.markdown(
        '<div class="section-title">Product Performance</div>',
        unsafe_allow_html=True
    )

    products = (
        filtered_df
        .groupby("product_name", as_index=False)
        .agg(
            Revenue=("revenue", "sum"),
            Profit=("profit", "sum"),
            Quantity=("quantity", "sum"),
            Orders=("order_id", "nunique")
        )
    )

    products["Profit_Margin"] = (
        products["Profit"]
        / products["Revenue"]
        * 100
    )

    top_products = products.sort_values(
        "Revenue",
        ascending=False
    ).head(10)

    bottom_products = products.sort_values(
        "Revenue",
        ascending=True
    ).head(10)

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            top_products.sort_values("Revenue"),
            x="Revenue",
            y="product_name",
            orientation="h",
            title="Top 10 Products by Revenue"
        )

        fig.update_layout(height=500)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.bar(
            bottom_products.sort_values("Revenue"),
            x="Revenue",
            y="product_name",
            orientation="h",
            title="Bottom 10 Products by Revenue"
        )

        fig.update_layout(height=500)

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    st.markdown("### Product Performance Table")

    display_products = products.sort_values(
        "Revenue",
        ascending=False
    ).copy()

    display_products["Revenue"] = display_products["Revenue"].round(2)
    display_products["Profit"] = display_products["Profit"].round(2)
    display_products["Profit_Margin"] = display_products["Profit_Margin"].round(2)

    st.dataframe(
        display_products,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# TAB 3 - CUSTOMER ANALYSIS
# =========================================================

with tab3:

    st.markdown(
        '<div class="section-title">Customer Analytics</div>',
        unsafe_allow_html=True
    )

    customers = (
        filtered_df
        .groupby("customer_id", as_index=False)
        .agg(
            Revenue=("revenue", "sum"),
            Profit=("profit", "sum"),
            Orders=("order_id", "nunique"),
            Quantity=("quantity", "sum")
        )
    )

    customers["Average_Order_Value"] = (
        customers["Revenue"]
        / customers["Orders"]
    )

    # Customer segmentation
    q1 = customers["Revenue"].quantile(0.33)
    q2 = customers["Revenue"].quantile(0.66)

    def segment_customer(value):

        if value <= q1:
            return "Low Value"

        elif value <= q2:
            return "Medium Value"

        return "High Value"

    customers["Segment"] = customers["Revenue"].apply(
        segment_customer
    )

    col1, col2 = st.columns(2)

    with col1:

        segment_count = (
            customers["Segment"]
            .value_counts()
            .reset_index()
        )

        segment_count.columns = [
            "Segment",
            "Customers"
        ]

        fig = px.pie(
            segment_count,
            names="Segment",
            values="Customers",
            title="Customer Segmentation"
        )

        fig.update_layout(height=400)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        segment_revenue = (
            customers
            .groupby("Segment", as_index=False)
            ["Revenue"]
            .sum()
        )

        fig = px.bar(
            segment_revenue,
            x="Segment",
            y="Revenue",
            title="Revenue by Customer Segment",
            text_auto=".2s"
        )

        fig.update_layout(height=400)

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    st.markdown("### 🏆 Top Customers")

    top_customers = customers.sort_values(
        "Revenue",
        ascending=False
    ).head(10)

    st.dataframe(
        top_customers,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# TAB 4 - REGIONAL ANALYSIS
# =========================================================

with tab4:

    st.markdown(
        '<div class="section-title">Regional Performance</div>',
        unsafe_allow_html=True
    )

    regional = (
        filtered_df
        .groupby("state", as_index=False)
        .agg(
            Revenue=("revenue", "sum"),
            Profit=("profit", "sum"),
            Orders=("order_id", "nunique"),
            Customers=("customer_id", "nunique")
        )
        .sort_values("Revenue", ascending=False)
    )

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            regional.head(10).sort_values("Revenue"),
            x="Revenue",
            y="state",
            orientation="h",
            title="Top 10 States by Revenue"
        )

        fig.update_layout(height=500)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.scatter(
            regional,
            x="Orders",
            y="Revenue",
            size="Customers",
            hover_name="state",
            title="Orders vs Revenue by State"
        )

        fig.update_layout(height=500)

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    st.markdown("### Regional Performance Table")

    st.dataframe(
        regional,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# TAB 5 - BUSINESS INSIGHTS
# =========================================================

with tab5:

    st.markdown(
        '<div class="section-title">💡 Automated Business Insights</div>',
        unsafe_allow_html=True
    )

    # Top category
    top_category = (
        category.sort_values(
            "Revenue",
            ascending=False
        ).iloc[0]
    )

    # Top product
    top_product = (
        products.sort_values(
            "Revenue",
            ascending=False
        ).iloc[0]
    )

    # Top state
    top_state = (
        regional.sort_values(
            "Revenue",
            ascending=False
        ).iloc[0]
    )

    # Highest profit category
    profit_category = (
        category.sort_values(
            "Profit",
            ascending=False
        ).iloc[0]
    )

    # High-value customers
    high_value_count = (
        customers[customers["Segment"] == "High Value"]
        .shape[0]
    )

    insights = [

        (
            "🏆",
            "Top Revenue Category",
            f"{top_category['category']} generated "
            f"₹{top_category['Revenue']:,.0f} in revenue."
        ),

        (
            "📦",
            "Best-Selling Product",
            f"{top_product['product_name']} generated "
            f"₹{top_product['Revenue']:,.0f} in revenue."
        ),

        (
            "🌎",
            "Top Performing State",
            f"{top_state['state']} generated "
            f"₹{top_state['Revenue']:,.0f} in revenue."
        ),

        (
            "💰",
            "Highest Profit Category",
            f"{profit_category['category']} generated "
            f"₹{profit_category['Profit']:,.0f} profit."
        ),

        (
            "👥",
            "High-Value Customers",
            f"{high_value_count:,} customers are classified "
            f"as high-value customers."
        ),

        (
            "📊",
            "Average Order Value",
            f"The current average order value is "
            f"₹{average_order_value:,.2f}."
        )

    ]

    for icon, title, description in insights:

        st.markdown(
            f"""
            <div class="insight-box">
                <strong>{icon} {title}</strong><br>
                {description}
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "E-Commerce Sales & Customer Analytics | "
    "Python • Pandas • SQL • Plotly • Streamlit"
)

st.caption(
    f"Showing {len(filtered_df):,} records after applying filters."
)