import numpy as np
import pandas as pd
import yfinance as yf

def rma(series, length):
    """Wilder's smoothing (RMA)"""
    alpha = 1 / length
    return series.ewm(alpha=alpha, adjust=False).mean()

def wma(series, length):
    """Weighted Moving Average"""
    weights = np.arange(1, length + 1)
    def calc_wma(x):
        return np.dot(x, weights) / weights.sum()
    return series.rolling(length).apply(calc_wma, raw=True)

def ma_function(series, length, smoothing='RMA'):
    smoothing = smoothing.upper()
    if smoothing == 'RMA':
        return rma(series, length)
    elif smoothing == 'SMA':
        return series.rolling(window=length).mean()
    elif smoothing == 'EMA':
        return series.ewm(span=length, adjust=False).mean()
    elif smoothing == 'WMA':
        return wma(series, length)
    else:
        raise ValueError(f"Unknown smoothing method: {smoothing}")

def true_range(df):
    high = df['High']
    low = df['Low']
    close = df['Close']

    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()

    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return tr

# Example usage
df = yf.download("KCHOL.IS", period="6mo", interval="1h")

length = 14
smoothing_method = 'RMA'  # Change to 'SMA', 'EMA', or 'WMA' if you want

df['ATR_14'] = ma_function(true_range(df), length, smoothing=smoothing_method)

print(df[['High', 'Low', 'Close', 'ATR_14']].tail(10))
