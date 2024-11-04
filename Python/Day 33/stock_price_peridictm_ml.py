import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dropout, Dense

# Loading the stock price
data = pd.DataFrame({
    "Date": ["2024-10-01", "2024-10-02", "2024-10-03", "2024-10-04", "2024-10-05", "2024-10-06", "2024-10-07", "2024-10-08"],
    "Close": [200.0, 202.5, 204.8, 207.0, 206.0, 208.5, 210.3, 209.0]
})
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)
dataset = data[['Close']].values

# Scale data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(dataset)

# Define a smaller sequence length for small dataset
sequence_length = 3

# Prepare training data
train_data_len = int(len(scaled_data) * 0.8)
train_data = scaled_data[:train_data_len]
x_train, y_train = [], []
for i in range(sequence_length, len(train_data)):
    x_train.append(train_data[i-sequence_length:i])
    y_train.append(train_data[i])

# Convert to numpy arrays and reshape for LSTM input
x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

# Build the LSTM model
model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)),
    Dropout(0.2),
    LSTM(50, return_sequences=False),
    Dropout(0.2),
    Dense(25),
    Dense(1)
])

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(x_train, y_train, batch_size=1, epochs=10)

# Prepare test data
test_data = scaled_data[train_data_len - sequence_length:]
x_test, y_test = [], dataset[train_data_len:]
for i in range(sequence_length, len(test_data)):
    x_test.append(test_data[i-sequence_length:i])

x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

# Make predictions and scale them back
predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

# Plot results
plt.figure(figsize=(12,6))
plt.plot(data.index, data['Close'], label='Actual Prices')
plt.plot(data.index[train_data_len:], predictions, label='Predicted Prices', linestyle='dashed')
plt.xlabel("Date")
plt.ylabel("Close Price (INR)")
plt.legend()
plt.show()
