import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import date
from statsmodels.tsa.seasonal import seasonal_decompose
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller

# Title
st.title("📈 Stock Forecasting using ARIMA")
st.subheader("Select a stock and forecast its future closing price using ARIMA model")

# Sidebar inputs
st.sidebar.title("Settings")
start_date = st.sidebar.date_input("Start Date", date(2020, 1, 1))
end_date = st.sidebar.date_input("End Date", date(2023, 12, 31))
ticker_list = ["AAPL", "MSFT", "GOOG", "TSLA", "AMZN", "NVDA"]
ticker = st.sidebar.selectbox("Select Ticker", ticker_list)

# Download data
data = yf.download(ticker, start=start_date, end=end_date)
data.reset_index(inplace=True)

# Show data
st.write(f"### {ticker} Stock Data")
st.dataframe(data.tail())

# Plot closing price
st.write("### Closing Price Over Time")
fig = px.line(data, x='Date', y='Close', title=f"{ticker} Closing Price")
st.plotly_chart(fig)

# Check stationarity
st.write("### Is Data Stationary?")
adf_result = adfuller(data["Close"])
st.write(f"ADF Statistic: {adf_result[0]}")
st.write(f"p-value: {adf_result[1]}")
if adf_result[1] < 0.05:
    st.success("✅ The data is stationary")
else:
    st.warning("⚠️ The data is not stationary. Consider differencing or transformation.")

# Decompose
st.write("### Time Series Decomposition")
decomposition = seasonal_decompose(data["Close"], model='additive', period=30)
fig_trend = px.line(x=data["Date"], y=decomposition.trend, title="Trend")
fig_seasonal = px.line(x=data["Date"], y=decomposition.seasonal, title="Seasonality")
fig_resid = px.line(x=data["Date"], y=decomposition.resid, title="Residual")
st.plotly_chart(fig_trend)
st.plotly_chart(fig_seasonal)
st.plotly_chart(fig_resid)

# ARIMA parameters
st.sidebar.markdown("### ARIMA Parameters")
p = st.sidebar.slider("AR (p)", 0, 5, 2)
d = st.sidebar.slider("I (d)", 0, 2, 1)
q = st.sidebar.slider("MA (q)", 0, 5, 2)

# Forecast horizon
forecast_days = st.sidebar.slider("Forecast Days", 1, 60, 15)

# Fit ARIMA model
model = sm.tsa.ARIMA(data["Close"], order=(p, d, q))
model_fit = model.fit()

# Forecast
forecast = model_fit.forecast(steps=forecast_days)
forecast_dates = pd.date_range(start=data["Date"].iloc[-1] + pd.Timedelta(days=1), periods=forecast_days)
forecast_df = pd.DataFrame({"Date": forecast_dates, "Forecast": forecast})

# Show forecast
st.write("### Forecasted Closing Prices")
st.dataframe(forecast_df)

# Plot forecast
fig_forecast = go.Figure()
fig_forecast.add_trace(go.Scatter(x=data["Date"], y=data["Close"], name="Historical"))
fig_forecast.add_trace(go.Scatter(x=forecast_df["Date"], y=forecast_df["Forecast"], name="Forecast", line=dict(color="red")))
fig_forecast.update_layout(title="ARIMA Forecast", xaxis_title="Date", yaxis_title="Price")
st.plotly_chart(fig_forecast)