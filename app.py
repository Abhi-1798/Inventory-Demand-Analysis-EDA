
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
stock_status = st.sidebar.multiselect("Select Stock Status", options=sorted(df["Stock Status"].unique()), default=sorted(df["Stock Status"].unique()))
date_range = st.sidebar.date_input("Select Date Range", [df["Date"].min(), df["Date"].max()])

# Filter data
filtered_df = df[
    (df["Category"].isin(category_options)) &
    (df["Region"].isin(region_options)) &
    (df["Weather Condition"].isin(weather_options)) &
    (df["Seasonality"].isin(season_options)) &
    (df["Stock Status"].isin(stock_status)) &
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

st.subheader("📦 Stock Status Distribution Over Time")
st.plotly_chart(px.histogram(df, x='Date', color='Stock Status',
                        title='Stock Status Distribution', barmode='stack'), use_container_width=True)

st.subheader("❌ Stock-Out Frequency Over Time")
stock_out_df = df[df['Stock Status'] == 'Stockout']
st.plotly_chart(px.histogram(stock_out_df, x='Date',
                        title='❌ Stock-Out Frequency'), use_container_width=True)

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

st.subheader("📆 Units Sold by Month and Day of Week")
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
month_order = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']
df['Weekday'] = pd.Categorical(df['Date'].dt.day_name(), categories=weekday_order, ordered=True)
df['Month'] = pd.Categorical(df['Date'].dt.month_name(), categories=month_order, ordered=True)
heat_data = df.groupby(['Month', 'Weekday'])['Units Sold'].sum().unstack()
st.plotly_chart(px.imshow(heat_data, 
                          title='Units Sold by Month and Day of Week', aspect="auto", 
                          labels=dict(color="Units Sold")), use_container_width=True)

st.subheader("💹 Revenue Over Time")
st.plotly_chart(px.line(df, x='Date', y='Revenue', title='💹 Revenue Over Time'), use_container_width=True)

st.subheader("📆 Monthly Revenue Trend")
df['Month'] = df['Date'].dt.to_period('M').astype(str)
monthly_rev = df.groupby('Month')['Revenue'].sum().reset_index()
monthly_rev['Month'] = pd.to_datetime(monthly_rev['Month'])
monthly_rev = monthly_rev.sort_values('Month')
monthly_rev['Month'] = monthly_rev['Month'].dt.strftime('%b %Y')
st.plotly_chart(px.bar(monthly_rev, x='Month', y='Revenue',
                            title='Monthly Revenue Trend'), use_container_width=True)

st.subheader("💸 Revenue vs Discount")
st.plotly_chart(px.scatter(df, x='Discount', y='Revenue',
                            title='Revenue vs Discount Trend Line', trendline='ols'), use_container_width=True)

