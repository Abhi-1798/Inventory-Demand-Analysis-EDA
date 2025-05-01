
import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Inventory Demand Dashboard", layout="wide")

st.title("📊 Inventory Demand Analysis Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("inventory_demand.csv")
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filters")

category_options = st.sidebar.multiselect("Select Category", options=sorted(df["Category"].unique()), default=sorted(df["Category"].unique()))
region_options = st.sidebar.multiselect("Select Region", options=sorted(df["Region"].unique()), default=sorted(df["Region"].unique()))
weather_options = st.sidebar.multiselect("Select Weather Condition", options=sorted(df["Weather Condition"].unique()), default=sorted(df["Weather Condition"].unique()))
season_options = st.sidebar.multiselect("Select Seasonality", options=sorted(df["Seasonality"].unique()), default=sorted(df["Seasonality"].unique()))
date_range = st.sidebar.date_input("Select Date Range", [df["Date"].min(), df["Date"].max()])

# Filter data
filtered_df = df[
    (df["Category"].isin(category_options)) &
    (df["Region"].isin(region_options)) &
    (df["Weather Condition"].isin(weather_options)) &
    (df["Seasonality"].isin(season_options)) &
    (df["Date"] >= pd.to_datetime(date_range[0])) &
    (df["Date"] <= pd.to_datetime(date_range[1]))
]

# Charts
st.subheader("📈 Units Sold Over Time (Daily)")
daily_sales = filtered_df.groupby('Date')['Units Sold'].sum().reset_index()
st.plotly_chart(px.line(daily_sales, x='Date', y='Units Sold', title='Daily Units Sold'), use_container_width=True)

st.subheader("📈 Units Sold Over Time (Monthly)")
monthly_sales = filtered_df.groupby(filtered_df['Date'].dt.to_period('M'))['Units Sold'].sum().reset_index()
monthly_sales['Date'] = monthly_sales['Date'].astype(str)
st.plotly_chart(px.line(monthly_sales, x='Date', y='Units Sold', title='Monthly Units Sold'), use_container_width=True)

st.subheader("🏆 Top Performing Product Categories")
cat_perf = filtered_df.groupby('Category')['Units Sold'].sum().sort_values(ascending=False)
st.plotly_chart(px.bar(cat_perf, x=cat_perf.index, y=cat_perf.values,
                       labels={'x': 'Category', 'y': 'Units Sold'},
                       title='Top Performing Categories'), use_container_width=True)

st.subheader("🌍 Sales Distribution by Region")
region_sales = filtered_df.groupby('Region')['Units Sold'].sum()
st.plotly_chart(px.pie(names=region_sales.index, values=region_sales.values,
                       title='Sales Distribution by Region'), use_container_width=True)



st.subheader("📊 Demand Forecast vs Actual Sales")
st.plotly_chart(px.scatter(filtered_df, x='Demand Forecast', y='Units Sold',
                           title="Demand Forecast vs Actual Sales", trendline="ols"), use_container_width=True)

st.subheader("☁️ Weather Condition vs Units Sold")
weather_sales = filtered_df.groupby('Weather Condition')['Units Sold'].mean().sort_values(ascending=False)
st.plotly_chart(px.bar(weather_sales, x=weather_sales.index, y=weather_sales.values,
                       title='Weather Condition vs Units Sold',
                       labels={'x': 'Weather Condition', 'y': 'Average Units Sold'}), use_container_width=True)

st.subheader("📦 Inventory Level vs Units Sold")
st.plotly_chart(px.scatter(filtered_df, x='Inventory Level', y='Units Sold',
                           title='Inventory Level vs Units Sold', trendline='ols'), use_container_width=True)

st.subheader("📅 Seasonality vs Units Sold")
season_sales = filtered_df.groupby('Seasonality')['Units Sold'].mean().sort_values(ascending=False)
st.plotly_chart(px.bar(season_sales, x=season_sales.index, y=season_sales.values,
                       title='Seasonality vs Units Sold',
                       labels={'x': 'Seasonality', 'y': 'Average Units Sold'}), use_container_width=True)
