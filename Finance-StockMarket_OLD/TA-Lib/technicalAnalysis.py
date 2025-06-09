import yfinance as yf
import pandas as pd
from finta import TA
import matplotlib.pyplot as plt

# Download historical data for a stock (e.g., Microsoft Corp.)
symbol = 'MSFT'
data = yf.download(symbol, start='2023-01-01', end='2024-01-01')

# Display the first few rows of the data
print(data.head())

# Calculate technical indicators using finta
data['SMA_50'] = TA.SMA(data, 50)  # 50-day Simple Moving Average
data['EMA_50'] = TA.EMA(data, 50)  # 50-day Exponential Moving Average
data['RSI'] = TA.RSI(data, 14)      # 14-day Relative Strength Index

# Calculate MACD
macd_values = TA.MACD(data)
data['MACD'] = macd_values['MACD']  # Use 'MACD'
data['Signal'] = macd_values['SIGNAL']  # Use 'SIGNAL'

# Calculate Bollinger Bands manually
window = 20  # Set the rolling window for Bollinger Bands
data['Middle_BB'] = data['Close'].rolling(window).mean()  # Middle Band
data['Upper_BB'] = data['Middle_BB'] + (data['Close'].rolling(window).std() * 2)  # Upper Band
data['Lower_BB'] = data['Middle_BB'] - (data['Close'].rolling(window).std() * 2)  # Lower Band

# Calculate Stochastic Oscillator
stochastic_values = TA.STOCH(data)

# Check the output to inspect
print(stochastic_values.head())  # Inspect the output
data['Stochastic_K'] = stochastic_values['14 period STOCH %K']
data['Stochastic_D'] = stochastic_values['14 period STOCH %D']

# Display the last few rows of the data with indicators
print(data[['Close', 'SMA_50', 'EMA_50', 'RSI', 'MACD', 'Signal', 'Upper_BB', 'Lower_BB', 'Stochastic_K', 'Stochastic_D']].tail())

# Optionally, visualize the indicators using matplotlib
plt.figure(figsize=(14, 12))

# Plot closing price and SMA
plt.subplot(4, 1, 1)
plt.plot(data['Close'], label='Close Price', color='blue')
plt.plot(data['SMA_50'], label='50-day SMA', color='orange')
plt.title('MSFT Price and 50-day SMA')
plt.legend()

# Plot MACD
plt.subplot(4, 1, 2)
plt.plot(data['MACD'], label='MACD', color='brown')
plt.plot(data['Signal'], label='Signal', color='orange')  # Optional
plt.title('MSFT MACD')
plt.legend()

# Plot Bollinger Bands
plt.subplot(4, 1, 3)
plt.plot(data['Close'], label='Close Price', color='blue')
plt.plot(data['Upper_BB'], label='Upper BB', color='green')
plt.plot(data['Middle_BB'], label='Middle BB', color='orange')
plt.plot(data['Lower_BB'], label='Lower BB', color='red')
plt.title('MSFT Bollinger Bands')
plt.legend()

# Plot Stochastic Oscillator
plt.subplot(4, 1, 4)
plt.plot(data['Stochastic_K'], label='Stochastic %K', color='purple')
plt.plot(data['Stochastic_D'], label='Stochastic %D', color='orange')  # Optional
plt.axhline(80, linestyle='--', alpha=0.5, color='red')
plt.axhline(20, linestyle='--', alpha=0.5, color='green')
plt.title('MSFT Stochastic Oscillator')
plt.legend()

plt.tight_layout()
plt.show()
