import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import statsmodels.api as sm
from datetime import date

st.title("📈 Stock Forecasting using ARIMA")
st.write("Select a stock and forecast its future closing price using ARIMA model")

# Sidebar
ticker = st.sidebar.selectbox("Select Stock", ["AAPL", "MSFT", "GOOG", "META", "TSLA"])
start_date = st.sidebar.date_input("Start Date", date(2020, 1, 1))
end_date = st.sidebar.date_input("End Date", date(2023, 12, 31))

# Load data
data = yf.download(ticker, start=start_date, end=end_date)

# ⛔️ Stop if data is empty
if data.empty:
    st.error("❌ No data found. Please select a valid ticker or change date range.")
    st.stop()

# Reset index to access 'Date'
data.reset_index(inplace=True)

# Show data
st.subheader(f"{ticker} Stock Data")
st.write(data.tail())

# Plot closing price
st.subheader("Closing Price Over Time")
fig = px.line(data, x='Date', y='Close', title=f"{ticker} Closing Price")
st.plotly_chart(fig)