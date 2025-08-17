import numpy as np
import pandas as pd
import yfinance as yf

def rma(series, length):
    alpha = 1 / length
    return series.ewm(alpha=alpha, adjust=False).mean()

def wma(series, length):
    weights = np.arange(1, length + 1)
    def calc_wma(x):
        return np.dot(x, weights) / weights.sum()
    return series.rolling(length).apply(calc_wma, raw=True)

def vwma(price, volume, length):
    pv = price * volume
    return pv.rolling(length).sum() / volume.rolling(length).sum()

def ma(source, length, ma_type, volume=None):
    ma_type = ma_type.upper()
    if ma_type == "SMA":
        return source.rolling(window=length).mean()
    elif ma_type == "EMA":
        return source.ewm(span=length, adjust=False).mean()
    elif ma_type == "SMMA (RMA)":
        return rma(source, length)
    elif ma_type == "WMA":
        return wma(source, length)
    elif ma_type == "VWMA":
        if volume is None:
            raise ValueError("Volume data required for VWMA")
        return vwma(source, volume, length)
    else:
        raise ValueError(f"Unknown MA type: {ma_type}")

# Download data for KCHOL.IS
df = yf.download("KCHOL.IS", period="6mo", interval="1h")

length = 20
ma_type = "SMA"  # Can be changed to EMA, SMMA (RMA), WMA, VWMA
mult = 2.0
src = df['Close']
volume = df['Volume']  # needed for VWMA

basis = ma(src, length, ma_type, volume)
dev = mult * src.rolling(window=length).std()

upper = basis + dev
lower = basis - dev

df['BB_Basis'] = basis
df['BB_Upper'] = upper
df['BB_Lower'] = lower

print(df[['Close', 'BB_Basis', 'BB_Upper', 'BB_Lower']].tail(10))
