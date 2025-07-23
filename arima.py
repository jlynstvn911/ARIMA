import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime, timedelta

st.set_page_config(page_title="ARIMA Stock Forecasting", layout="centered")

st.title("📈 Stock Price Forecasting with ARIMA")
st.write("Upload your Excel file with 'Date' and 'Close' columns.")

# Upload Excel
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    # Check required columns
    if 'Date' not in df.columns or 'Close' not in df.columns:
        st.error("Excel must contain 'Date' and 'Close' columns.")
    else:
        # Parse date and sort
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')
        df.set_index('Date', inplace=True)

        st.subheader("Raw Data")
        st.line_chart(df['Close'])

        # Forecasting
        st.subheader("ARIMA Forecasting")
        periods = st.slider("Forecast Period (months)", 1, 24, 6)

        try:
            model = ARIMA(df['Close'], order=(2, 1, 2))  # You can tune the order
            model_fit = model.fit()
            forecast = model_fit.forecast(steps=periods)

            # Buat tanggal untuk forecast
            last_date = df.index[-1]
            forecast_dates = [last_date + timedelta(days=30 * i) for i in range(1, periods + 1)]

            forecast_df = pd.DataFrame({'Date': forecast_dates, 'Forecast': forecast})
            forecast_df.set_index('Date', inplace=True)

            # Gabungkan data asli dan prediksi
            combined_df = pd.concat([df['Close'], forecast_df['Forecast']])

            st.line_chart(combined_df)

            st.write("Forecast Table:")
            st.dataframe(forecast_df)

        except Exception as e:
            st.error(f"Model Error: {e}")