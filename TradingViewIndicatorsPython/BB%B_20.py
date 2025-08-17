#Chart based appearence maybe we can improve it for data based.
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Download data
df = yf.download("KCHOL.IS", period="2mo", interval="1h")

length = 20
mult = 2.0
src = df['Close']

# Calculate Bollinger Bands
basis = src.rolling(window=length).mean()
dev = mult * src.rolling(window=length).std()
upper = basis + dev
lower = basis - dev

# Calculate %b
bbr = (src - lower) / (upper - lower)

df['BB_b'] = bbr

# Plot %b with background colors similar to TradingView
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['BB_b'], label="BB %b", color="#2962FF")
plt.axhline(1, color="#F23645", linestyle="--", alpha=0.5, label="Overbought")
plt.axhline(0.5, color="#2962FF", alpha=0.5, label="Middle Band")
plt.axhline(0, color="#089981", linestyle="--", alpha=0.5, label="Oversold")

plt.fill_between(df.index, 0, 1, color="#2962FF", alpha=0.1)  # Middle band background
plt.fill_between(df.index, 1, 2, color="#F23645", alpha=0.1)  # Overbought background
plt.fill_between(df.index, -1, 0, color="#089981", alpha=0.1)  # Oversold background

plt.title("Bollinger Bands %b for KCHOL.IS")
plt.legend()
plt.show()
