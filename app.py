# app.py
import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
import joblib
from datetime import datetime

st.title("📈 Stock Price Forecasting with GRU")

# Input user
ticker = st.text_input("Enter stock ticker (e.g. GOTO.JK, BBCA.JK):", "GOTO.JK")

# Load data
start_date = "2020-01-01"
end_date = datetime.today().strftime('%Y-%m-%d')

data = yf.download(ticker, start=start_date, end=end_date)
st.write("Raw data", data.tail())

# Visualisasi harga
st.subheader('Closing Price Chart')
fig, ax = plt.subplots()
ax.plot(data['Close'])
st.pyplot(fig)

# Tombol untuk prediksi (bisa kamu lanjutkan nanti)
if st.button('Run GRU Forecast'):
    st.info("Model not loaded yet. This is just a placeholder.")