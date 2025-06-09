import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt



# Define the stock symbol and time period
symbol = "TSLA"
start_date = "2022-01-01"
end_date = "2023-01-01"

# Download historical data
data = yf.download(symbol, start=start_date, end=end_date)

# Define breakout level (you can use other methods to dynamically find this)
breakout_level = data['Close'].rolling(window=20).max()  # Using 20-day high as breakout level

# Generate buy/sell signals based on breakout levels
data['Signal'] = 0  # 0 means no signal, 1 means buy, -1 means sell
data.loc[data['Close'] > breakout_level, 'Signal'] = 1
data.loc[data['Close'] < breakout_level, 'Signal'] = -1

# Plot the closing price and breakout level
plt.figure(figsize=(12, 6))
plt.plot(data['Close'], label='Close Price', alpha=0.5)
plt.plot(breakout_level, label='Breakout Level', linestyle='--')

# Plot buy signals
plt.plot(data[data['Signal'] == 1].index, 
         data['Close'][data['Signal'] == 1],
         '^', markersize=10, color='g', label='Buy Signal')

# Plot sell signals
plt.plot(data[data['Signal'] == -1].index, 
         data['Close'][data['Signal'] == -1],
         'v', markersize=10, color='r', label='Sell Signal')

plt.title(f'{symbol} Stock Price with Breakout Trading Strategy')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.legend()
plt.show()
