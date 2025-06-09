import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Define the stock symbol and time period
symbol = "AAPL"
start_date = "2022-01-01"
end_date = "2023-01-01"

# Download historical data
data = yf.download(symbol, start=start_date, end=end_date)

# Define support and resistance levels (you can use other methods to dynamically find these)
support_level = data['Close'].rolling(window=20).min()  # Using 20-day low as support level
resistance_level = data['Close'].rolling(window=20).max()  # Using 20-day high as resistance level

# Generate buy/sell signals based on support and resistance levels
data['Signal'] = 0  # 0 means no signal, 1 means buy, -1 means sell
data.loc[data['Close'] < support_level, 'Signal'] = 1
data.loc[data['Close'] > resistance_level, 'Signal'] = -1

# Plot the closing price, support, and resistance levels
plt.figure(figsize=(12, 6))
plt.plot(data['Close'], label='Close Price', alpha=0.5)
plt.plot(support_level, label='Support Level', linestyle='--')
plt.plot(resistance_level, label='Resistance Level', linestyle='--')

# Plot buy signals
plt.plot(data[data['Signal'] == 1].index, 
         data['Close'][data['Signal'] == 1],
         '^', markersize=10, color='g', label='Buy Signal')

# Plot sell signals
plt.plot(data[data['Signal'] == -1].index, 
         data['Close'][data['Signal'] == -1],
         'v', markersize=10, color='r', label='Sell Signal')

plt.title(f'{symbol} Stock Price with Range-Bound Trading Strategy')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.legend()
plt.show()
