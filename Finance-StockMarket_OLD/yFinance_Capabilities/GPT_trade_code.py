import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Define the stock symbol and time period
symbol = "TSLA"
start_date = "2022-01-01"
end_date = "2023-01-01"

# Download historical data
data = yf.download(symbol, start=start_date, end=end_date)

# Calculate short-term (fast) and long-term (slow) moving averages
data['Short_MA'] = data['Close'].rolling(window=20).mean()  # Adjust window size as needed
data['Long_MA'] = data['Close'].rolling(window=50).mean()   # Adjust window size as needed

# Generate buy/sell signals based on moving average crossovers
data['Signal'] = 0  # 0 means no signal, 1 means buy, -1 means sell
data.loc[data['Short_MA'] > data['Long_MA'], 'Signal'] = 1
data.loc[data['Short_MA'] < data['Long_MA'], 'Signal'] = -1

# Plot the closing price and moving averages
plt.figure(figsize=(12, 6))
plt.plot(data['Close'], label='Close Price', alpha=0.5)
plt.plot(data['Short_MA'], label='Short MA', linestyle='--')
plt.plot(data['Long_MA'], label='Long MA', linestyle='--')

# Plot buy signals
plt.plot(data[data['Signal'] == 1].index, 
         data['Short_MA'][data['Signal'] == 1],
         '^', markersize=10, color='g', label='Buy Signal')

# Plot sell signals
plt.plot(data[data['Signal'] == -1].index, 
         data['Short_MA'][data['Signal'] == -1],
         'v', markersize=10, color='r', label='Sell Signal')

plt.title(f'{symbol} Stock Price with Trend Following Strategy')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.legend()
plt.show()
