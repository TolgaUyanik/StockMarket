# It seems good. Need to learn what are the capabilities & how to use.
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Download data
df = yf.download("KCHOL.IS", period="2mo", interval="1h")

length = 20
mult = 2.0
expansion_length = 125
contraction_length = 125
src = df['Close']

# Calculate Bollinger Bands
basis = src.rolling(window=length).mean()
dev = mult * src.rolling(window=length).std()
upper = basis + dev
lower = basis - dev

# Calculate Bollinger BandWidth (BBW) in percent
bbw = ((upper - lower) / basis) * 100

# Highest Expansion over lookback window
highest_expansion = bbw.rolling(window=expansion_length).max()

# Lowest Contraction over lookback window
lowest_contraction = bbw.rolling(window=contraction_length).min()

df['BBW'] = bbw
df['Highest_Expansion'] = highest_expansion
df['Lowest_Contraction'] = lowest_contraction

# Plotting
plt.figure(figsize=(14, 6))
plt.plot(df.index, df['BBW'], label="Bollinger BandWidth", color="#2962FF")
plt.plot(df.index, df['Highest_Expansion'], label="Highest Expansion", color="#F2364580")  # 50% opacity
plt.plot(df.index, df['Lowest_Contraction'], label="Lowest Contraction", color="#08998180")  # 50% opacity

plt.title("Bollinger BandWidth (BBW) for KCHOL.IS")
plt.ylabel("BBW (%)")
plt.legend()
plt.show()
