import os
import pandas as pd
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
import streamlit as st

# Set Streamlit page title
st.set_page_config(page_title='Stock Price Analysis', page_icon='📈')

# Title and description
st.title('Stock Price Analysis App')
st.write('This app fetches and analyzes stock price data.')

# Sidebar
st.sidebar.header('User Input')

# Read the API key from the file
with open('api.txt', 'r') as file:
    api_key = file.readline().strip()

# Replace with your Alpha Vantage API key
api_key = api_key

# User input for stock symbol
symbol = st.sidebar.text_input('Enter Stock Symbol')
symbol = symbol.upper()

# User input for time interval
interval = st.sidebar.selectbox('Select Time Interval', ['1d', '1wk', '1mo', '1yr'])

# Fetch stock price data
ts = TimeSeries(key=api_key, output_format='pandas')
data, meta_data = ts.get_daily(symbol=symbol, outputsize='full')
data = data.iloc[::-1]  # Reverse data for chronological order

# Calculate daily returns
data['Daily_Return'] = data['4. close'].astype(float).pct_change()

# Display stock price data
st.subheader(f'Stock Price Data for {symbol}')
st.write(data)

# Create a folder for the stock analysis results
output_dir = 'stock_analysis'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    
analysis_dir = os.path.join(output_dir, symbol)
if not os.path.exists(analysis_dir):
    os.makedirs(analysis_dir)

# Save the stock price data to a CSV file
data.to_csv(os.path.join(analysis_dir, f'{symbol}_price_data.csv'), index=False)

# Plot the stock price chart
st.subheader(f'{symbol} Stock Price Chart')
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_title(f'{symbol} Stock Price')
ax.set_xlabel('Date')
ax.set_ylabel('Price (USD)')
ax.plot(data.index, data['4. close'].astype(float), label='Closing Price', color='blue')
ax.legend()
ax.grid(True)

# Save the stock price chart as an image
chart_file = os.path.join(analysis_dir, f'{symbol}_price_chart.png')
plt.savefig(chart_file)
st.pyplot(fig)

# Link to download data CSV
st.markdown(f"Download the stock price data as [CSV](/{analysis_dir}/{symbol}_price_data.csv)")

# Link to download chart image
st.markdown(f"Download the stock price chart as [PNG](/{analysis_dir}/{symbol}_price_chart.png)")
