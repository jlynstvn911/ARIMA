import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense
import joblib

# Ambil data
data = yf.download("BBRI.JK", start="2019-01-01", end="2023-12-31")['Close'].values
data = data.reshape(-1, 1)

# Normalize
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data)

# Save scaler
joblib.dump(scaler, "scaler.save")

# Buat dataset time-series
def create_dataset(data, time_step=10):
    X, y = [], []
    for i in range(len(data)-time_step):
        X.append(data[i:i+time_step])
        y.append(data[i+time_step])
    return np.array(X), np.array(y)

X, y = create_dataset(data_scaled)
X = X.reshape(X.shape[0], X.shape[1], 1)

# Bangun dan latih model GRU
model = Sequential()
model.add(GRU(50, return_sequences=False, input_shape=(X.shape[1], 1)))
model.add(Dense(1))
model.compile(loss='mse', optimizer='adam')
model.fit(X, y, epochs=20, batch_size=32, verbose=1)

# Simpan model
model.save("model_gru.h5")