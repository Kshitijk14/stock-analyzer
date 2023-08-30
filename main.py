import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries

# Read the API key from the file
with open('api.txt', 'r') as file:
    api_key = file.readline().strip()

# Replace with your Alpha Vantage API key
api_key = api_key

# Define the stock symbol and time period
symbol = input("Enter the symbol/ticker: ")
symbol = symbol.upper()
interval = '1d'  # Daily data

# Create a directory to store data and charts
output_dir = 'stock_analysis'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Initialize Alpha Vantage API client
ts = TimeSeries(key=api_key, output_format='pandas')

# Fetch stock price data
data, meta_data = ts.get_daily(symbol=symbol, outputsize='full')
data = data.iloc[::-1]  # Reverse data for chronological order

# Calculate daily returns
data['Daily_Return'] = data['4. close'].astype(float).pct_change()

# Create a folder for the stock analysis results
analysis_dir = os.path.join(output_dir, symbol)
if not os.path.exists(analysis_dir):
    os.makedirs(analysis_dir)

# Save the stock price data to a CSV file
data.to_csv(os.path.join(analysis_dir, f'{symbol}_price_data.csv'))

# Plot the stock price chart
plt.figure(figsize=(12, 6))
plt.title(f'{symbol} Stock Price')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.plot(data.index, data['4. close'].astype(float), label='Closing Price', color='blue')
plt.legend()
plt.grid(True)

# Save the stock price chart as an image
chart_file = os.path.join(analysis_dir, f'{symbol}_price_chart.png')
plt.savefig(chart_file)

# Show the chart
plt.show()
