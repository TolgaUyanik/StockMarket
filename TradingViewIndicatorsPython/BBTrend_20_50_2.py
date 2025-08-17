# Charts need some improvements. We can decide it later. We don't know the capabilities of this indicator yet.
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

def bollinger_bands(series, length, mult):
    basis = series.rolling(length).mean()
    dev = mult * series.rolling(length).std()
    upper = basis + dev
    lower = basis - dev
    return basis, upper, lower

# Download data
df = yf.download("KCHOL.IS", period="2mo", interval="1h")

short_len = 20
long_len = 50
mult = 2.0
close = df['Close']

# Short and Long BB
short_middle, short_upper, short_lower = bollinger_bands(close, short_len, mult)
long_middle, long_upper, long_lower = bollinger_bands(close, long_len, mult)

# Calculate BBTrend
bbtrend = ((short_lower - long_lower).abs() - (short_upper - long_upper).abs()) / short_middle * 100

# Create a DataFrame column for easier handling
df['BBTrend'] = bbtrend

# Calculate previous value shifted by 1 for comparison
df['BBTrend_prev'] = df['BBTrend'].shift(1)

def get_color(row):
    # Use .loc to get scalar, or convert Series with single value
    bbtrend = row['BBTrend']
    bbtrend_prev = row['BBTrend_prev']

    # If bbtrend or bbtrend_prev is a Series, get its scalar value
    if isinstance(bbtrend, pd.Series) or isinstance(bbtrend, np.ndarray):
        bbtrend = bbtrend.iloc[0] if hasattr(bbtrend, 'iloc') else bbtrend.item()
    if isinstance(bbtrend_prev, pd.Series) or isinstance(bbtrend_prev, np.ndarray):
        bbtrend_prev = bbtrend_prev.iloc[0] if hasattr(bbtrend_prev, 'iloc') else bbtrend_prev.item()

    if pd.isna(bbtrend) or pd.isna(bbtrend_prev):
        return '#08998180'

    if bbtrend > 0 and bbtrend >= bbtrend_prev:
        return '#08998140'
    elif bbtrend > 0 and bbtrend < bbtrend_prev:
        return '#08998180'
    elif bbtrend < 0 and bbtrend > bbtrend_prev:
        return '#F2364580'
    elif bbtrend < 0 and bbtrend <= bbtrend_prev:
        return '#F2364540'
    else:
        return '#08998180'



df['Color'] = df.apply(get_color, axis=1)


# Plotting
plt.figure(figsize=(14,6))
plt.bar(df.index, df['BBTrend'], color=df['Color'], width=0.8)
plt.axhline(0, color='black', linewidth=1, linestyle='--')
plt.title('BBTrend for KCHOL.IS')
plt.ylabel('BBTrend')
plt.show()
