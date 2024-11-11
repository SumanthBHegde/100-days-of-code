import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

# Load Dataset 
data = pd.read_csv('ecommerce_sales.csv')
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# Plot initial data to understand the time series
plt.figure(figsize=(10,6))
plt.plot(data['Sales'], label='Sales')
plt.title('Sales Over Time')
plt.xlabel('Date')
plt.ylabel('Sales')
plt.legend()
plt.show()

# Create lag features for capturing seasonal patterns
data['Sales_Lag_1'] = data['Sales'].shift(1)
data['Sales_Lag_7'] = data['Sales'].shift(7)

# Drop rows with missing values due to lag
data.dropna(inplace=True)

# Use the last 20% of data as a test set
train_size = int(len(data)*0.8)
train, test = data['Sales'][:train_size], data['Sales'][train_size:]

# Define and fit ARIMA model with an order of (5,1,0)
model = ARIMA(train, order=(5,1,0))
fitted_model = model.fit()

# Forecast on test data
forecast = fitted_model.forecast(steps=len(test))

# Calculate evaluation metrics
rmse = np.sqrt(mean_squared_error(test, forecast))
mae = mean_absolute_error(test, forecast)
print(f"Root Mean Squared Error (RMSE): {rmse}")
print(f"Mean Absolute Error (MAE): {mae}")

# Plot both the actual and forecasted sales values
plt.figure(figsize=(10,6))
plt.plot(train, label='Training Data')
plt.plot(test, label='Actual Sales')
plt.plot(test.index, forecast, label='Forecasted Sales', linestyle='--')
plt.title("E-commerce Sales Forecast")
plt.xlabel('Date')
plt.ylabel('Sales')
plt.legend()
plt.show()

