
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load custom CSS theme
with open("style.css", "r", encoding="utf-8") as css_file:
    st.markdown(
        f"<style>{css_file.read()}</style>",
        unsafe_allow_html=True
    )
st.title("📊 Sales Analytics Dashboard")
st.caption("Interactive business performance analysis")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("sales_data.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Dashboard Filters")

regions = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

categories = st.sidebar.multiselect(
    "Select Category",
    options=sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

filtered = df[
    df["Region"].isin(regions)
    & df["Category"].isin(categories)
]

if filtered.empty:
    st.warning("No data matches these filters.")
    st.stop()

# KPI metrics
total_sales = filtered["Sales"].sum()
total_profit = filtered["Profit"].sum()
total_orders = filtered["Order_ID"].nunique()
total_quantity = filtered["Quantity"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"₹{total_sales:,.0f}")
col2.metric("Total Profit", f"₹{total_profit:,.0f}")
col3.metric("Total Orders", f"{total_orders:,}")
col4.metric("Units Sold", f"{total_quantity:,}")

st.divider()

# Prepare monthly sales
monthly = (
    filtered.assign(
        Month=filtered["Date"].dt.to_period("M").astype(str)
    )
    .groupby("Month", as_index=False)["Sales"]
    .sum()
)

left, right = st.columns(2)

with left:
    st.subheader("Monthly Sales Trend")
    fig = px.line(
        monthly,
        x="Month",
        y="Sales",
        markers=True,
        title="Sales by Month"
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Sales by Region")
    region_sales = (
        filtered.groupby("Region", as_index=False)["Sales"]
        .sum()
    )
    fig = px.bar(
        region_sales,
        x="Region",
        y="Sales",
        color="Region",
        title="Regional Performance"
    )
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)

with left:
    st.subheader("Sales by Category")
    category_sales = (
        filtered.groupby("Category", as_index=False)["Sales"]
        .sum()
    )
    fig = px.pie(
        category_sales,
        names="Category",
        values="Sales",
        hole=0.4
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Profit by Product")
    product_profit = (
        filtered.groupby("Product", as_index=False)["Profit"]
        .sum()
        .sort_values("Profit", ascending=False)
    )
    fig = px.bar(
        product_profit,
        x="Product",
        y="Profit",
        title="Product Profitability"
    )
    st.plotly_chart(fig, use_container_width=True)

# Detailed data
st.subheader("Sales Data Explorer")
st.dataframe(
    filtered.sort_values("Date", ascending=False),
    use_container_width=True,
    hide_index=True
)

# Download filtered data
csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Sales Data",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)

st.caption("Portfolio project | Sample data for demonstration")