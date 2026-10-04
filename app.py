
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Retail Sales Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)


# ---------------------------------------------------------
# LOAD DATASET
# ---------------------------------------------------------

data_path = Path(__file__).parent / "sample - superstore.csv"

try:
    df = pd.read_csv(
        data_path,
        encoding="latin1"
    )

except FileNotFoundError:
    st.error(
        "Dataset not found. Make sure "
        "'sample - superstore.csv' is in the same folder as app.py."
    )
    st.stop()

except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()


# ---------------------------------------------------------
# SIDEBAR STYLE
# ---------------------------------------------------------

st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background-color: wheat;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# SIDEBAR MENU
# ---------------------------------------------------------

selected_page = st.sidebar.radio(
    "Select a page",
    [
        "Dashboard",
        "Dataset",
        "Visualization",
        "KPI Report"
    ]
)


# ---------------------------------------------------------
# COMMON CALCULATIONS
# ---------------------------------------------------------

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()


# =========================================================
# DASHBOARD
# =========================================================

if selected_page == "Dashboard":

    st.markdown(
        """
        <style>
            .dashboard-title {
                background: linear-gradient(
                    120deg,
                    #f4e5c7,
                    #fff8e8,
                    #e8c98c,
                    #fff8e8
                );
                border-radius: 14px;
                color: #5b3a13;
                padding: 18px 12px;
                text-align: center;
                font-size: 2rem;
                font-weight: 750;
                margin-bottom: 18px;
            }

            .dashboard-intro {
                background: linear-gradient(
                    120deg,
                    #f4e5c7,
                    #fff8e8,
                    #e8c98c,
                    #fff8e8
                );
                border-radius: 14px;
                color: #655744;
                padding: 18px 12px;
                text-align: center;
                line-height: 1.7;
                margin: 18px 0 24px;
            }

            .dashboard-intro strong {
                color: #9a5b0a;
                font-size: 1.2rem;
            }
        </style>

        <h1 class="dashboard-title">
            Retail Sales Analysis Dashboard
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown(
        """
        <div class="dashboard-intro">
            <strong>
                Welcome to Retail Sales Analysis Dashboard
            </strong>
            <br>
            This dashboard helps to analyze the sales data.
        </div>
        """,
        unsafe_allow_html=True
    )

    # KPI cards
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Profit",
            f"₹{total_profit:,.2f}"
        )

    with col2:
        st.metric(
            "Total Sales",
            f"₹{total_sales:,.2f}"
        )

    # Sales and Profit chart
    st.subheader("Sales vs Profit")

    chart_data = pd.DataFrame(
        {
            "Amount": [
                total_sales,
                total_profit
            ]
        },
        index=[
            "Total Sales",
            "Total Profit"
        ]
    )

    st.bar_chart(chart_data)


# =========================================================
# DATASET
# =========================================================

elif selected_page == "Dataset":

    st.subheader("Dataset Preview")

    # Dataset size
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Rows",
            f"{len(df):,}"
        )

    with col2:
        st.metric(
            "Total Columns",
            f"{len(df.columns):,}"
        )

    # Data preview
    st.subheader("View Dataset")

    number_of_rows = st.slider(
        "Number of rows to display",
        min_value=1,
        max_value=len(df),
        value=min(5, len(df))
    )

    st.dataframe(
        df.head(number_of_rows),
        use_container_width=True
    )

    # Null values
    st.subheader("Null Values")

    null_values = df.isnull().sum()

    st.dataframe(
        null_values.to_frame("Null Count"),
        use_container_width=True
    )

    if null_values.sum() == 0:
        st.success("No null values found.")
    else:
        st.warning(
            f"{null_values.sum()} null values found."
        )

    # Summary statistics
    st.subheader("Summary of Data")

    st.dataframe(
        df.describe(),
        use_container_width=True
    )


# =========================================================
# VISUALIZATION
# =========================================================

elif selected_page == "Visualization":

    st.markdown(
        "<h2 style='text-align: center;'>Visualization</h2>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Make a copy
    visual_df = df.copy()

    # Convert Order Date
    visual_df["Order Date"] = pd.to_datetime(
        visual_df["Order Date"],
        errors="coerce"
    )


    # -----------------------------------------------------
    # SALES BY MONTH
    # -----------------------------------------------------

    monthly_sales = (
        visual_df
        .dropna(subset=["Order Date"])
        .groupby(
            visual_df["Order Date"].dt.month
        )["Sales"]
        .sum()
    )

    st.header("Sales by Month")

    st.bar_chart(monthly_sales)

    if not monthly_sales.empty:
        highest_month = monthly_sales.idxmax()

        st.success(
            f"Highest Sales Month: {highest_month}"
        )


    # -----------------------------------------------------
    # PROFIT BY CATEGORY
    # -----------------------------------------------------

    category_profit = (
        visual_df
        .groupby("Category")["Profit"]
        .sum()
        .sort_values(ascending=False)
    )

    st.header("Profit by Category")

    st.bar_chart(category_profit)

    st.success(
        f"Most Profitable Category: "
        f"{category_profit.index[0]}"
    )

    st.info(
        f"Least Profitable Category: "
        f"{category_profit.index[-1]}"
    )


    # -----------------------------------------------------
    # PROFIT BY SUB-CATEGORY
    # -----------------------------------------------------

    sub_category_profit = (
        visual_df
        .groupby("Sub-Category")["Profit"]
        .sum()
        .sort_values(ascending=False)
    )

    st.header("Profit by Sub-Category")

    st.bar_chart(sub_category_profit)

    st.success(
        f"Most Profitable Sub-Category: "
        f"{sub_category_profit.index[0]}"
    )

    st.info(
        f"Least Profitable Sub-Category: "
        f"{sub_category_profit.index[-1]}"
    )


    # -----------------------------------------------------
    # TOP PRODUCTS
    # -----------------------------------------------------

    top_products = (
        visual_df
        .groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.header("Top 10 Products by Sales")

    st.bar_chart(top_products)

    st.success(
        f"Top Product: {top_products.index[0]}"
    )


    # -----------------------------------------------------
    # SALES BY SEGMENT
    # -----------------------------------------------------

    segment_sales = (
        visual_df
        .groupby("Segment")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    st.header("Sales by Segment")

    st.bar_chart(segment_sales)

    st.success(
        f"Top Segment: {segment_sales.index[0]}"
    )


    # -----------------------------------------------------
    # SALES BY REGION
    # -----------------------------------------------------

    region_sales = (
        visual_df
        .groupby("Region")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    st.header("Sales by Region")

    st.bar_chart(region_sales)

    st.success(
        f"Region with Highest Sales: "
        f"{region_sales.index[0]}"
    )


    # -----------------------------------------------------
    # PROFIT BY REGION
    # -----------------------------------------------------

    region_profit = (
        visual_df
        .groupby("Region")["Profit"]
        .sum()
        .sort_values(ascending=False)
    )

    st.header("Profit by Region")

    st.bar_chart(region_profit)

    st.success(
        f"Region with Highest Profit: "
        f"{region_profit.index[0]}"
    )


    # -----------------------------------------------------
    # PROFIT BY DISCOUNT
    # -----------------------------------------------------

    discount_profit = (
        visual_df
        .groupby("Discount")["Profit"]
        .sum()
        .sort_values()
    )

    st.header("Profit by Discount")

    st.bar_chart(discount_profit)

    st.info(
        "The chart shows how profit changes "
        "at different discount levels."
    )


    # -----------------------------------------------------
    # CORRELATION HEATMAP
    # -----------------------------------------------------

    st.header("Correlation Heatmap")

    correlation_columns = [
        "Sales",
        "Profit",
        "Quantity",
        "Discount"
    ]

    correlation_data = visual_df[
        correlation_columns
    ].corr()

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    sns.heatmap(
        correlation_data,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        ax=ax
    )

    ax.set_title(
        "Correlation Between Sales, Profit, "
        "Quantity and Discount"
    )

    st.pyplot(
        fig,
        use_container_width=True
    )

    plt.close(fig)


# =========================================================
# KPI REPORT
# =========================================================

elif selected_page == "KPI Report":

    # KPI calculations

    total_sales = df["Sales"].sum()

    total_profit = df["Profit"].sum()

    total_orders = df["Order ID"].nunique()

    total_customers = df["Customer ID"].nunique()

    average_sales = df["Sales"].mean()

    profit_margin = (
        total_profit / total_sales
    ) * 100


    # -----------------------------------------------------
    # TITLE
    # -----------------------------------------------------

    st.markdown(
        "<h2 style='text-align: center;'>KPI Report Card</h2>",
        unsafe_allow_html=True
    )

    st.markdown("---")


    # -----------------------------------------------------
    # KPI CARDS
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Sales",
            f"₹{total_sales:,.2f}"
        )

    with col2:
        st.metric(
            "Total Profit",
            f"₹{total_profit:,.2f}"
        )

    with col3:
        st.metric(
            "Total Orders",
            f"{total_orders:,}"
        )

    with col4:
        st.metric(
            "Total Customers",
            f"{total_customers:,}"
        )


    # -----------------------------------------------------
    # ADDITIONAL KPIs
    # -----------------------------------------------------

    st.subheader("Additional KPIs")

    col5, col6 = st.columns(2)

    with col5:
        st.metric(
            "Average Sale",
            f"₹{average_sales:,.2f}"
        )

    with col6:
        st.metric(
            "Profit Margin",
            f"{profit_margin:.2f}%"
        )


    # -----------------------------------------------------
    # TOP CATEGORY
    # -----------------------------------------------------

    top_category = (
        df
        .groupby("Category")["Sales"]
        .sum()
        .idxmax()
    )


    # -----------------------------------------------------
    # TOP PRODUCT
    # -----------------------------------------------------

    top_product = (
        df
        .groupby("Product Name")["Sales"]
        .sum()
        .idxmax()
    )


    # -----------------------------------------------------
    # TOP CUSTOMER
    # -----------------------------------------------------

    top_customer = (
        df
        .groupby("Customer Name")["Sales"]
        .sum()
        .idxmax()
    )


    # -----------------------------------------------------
    # TOP STATE
    # -----------------------------------------------------

    top_state = (
        df
        .groupby("State")["Sales"]
        .sum()
        .idxmax()
    )


    # -----------------------------------------------------
    # BUSINESS INSIGHTS
    # -----------------------------------------------------

    st.subheader("Business Insights")

    st.write(
        f"**Top Category:** {top_category}"
    )

    st.write(
        f"**Top Product:** {top_product}"
    )

    st.write(
        f"**Top Customer:** {top_customer}"
    )

    st.write(
        f"**Top State:** {top_state}"
    )

    st.write(
        f"**Profit Margin:** {profit_margin:.2f}%"
    )

    st.success(
        "KPI Report generated successfully."
    )

