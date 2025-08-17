#Little differences exist but nothing to worry for now.
import pandas as pd
import numpy as np
import yfinance as yf

# === Download sample data for KCHOL.IS ===
df = yf.download("KCHOL.IS", period="2mo", interval="1h")

# === Calculate hlc3 (typical price) ===
df["hlc3"] = (df["High"] + df["Low"] + df["Close"]) / 3

# === 1. Commodity Channel Index (CCI) ===
def mean_absolute_deviation(series):
    return np.mean(np.abs(series - np.mean(series)))

def cci(src, length=20):
    ma = src.rolling(length).mean()
    dev = src.rolling(length).apply(mean_absolute_deviation, raw=False)
    return (src - ma) / (0.015 * dev)

df["CCI"] = cci(df["hlc3"], length=20)

# === 2. Moving Average Types ===
def moving_average(series, length, ma_type, volume=None):
    if ma_type == "SMA":
        return series.rolling(length).mean()
    elif ma_type == "EMA":
        return series.ewm(span=length, adjust=False).mean()
    elif ma_type == "SMMA (RMA)":
        smma = series.copy()
        smma.iloc[length-1] = series.iloc[:length].mean()
        for i in range(length, len(series)):
            smma.iloc[i] = (smma.iloc[i-1] * (length - 1) + series.iloc[i]) / length
        return smma
    elif ma_type == "WMA":
        weights = np.arange(1, length+1)
        return series.rolling(length).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)
    elif ma_type == "VWMA" and volume is not None:
        return (series * volume).rolling(length).sum() / volume.rolling(length).sum()
    elif ma_type == "SMA + Bollinger Bands":
        return series.rolling(length).mean()
    else:
        return pd.Series([np.nan] * len(series), index=series.index)

# === User settings ===
ma_type_input = "SMA"  # Options: None, SMA, EMA, SMMA (RMA), WMA, VWMA, SMA + Bollinger Bands
ma_length_input = 14
bb_mult_input = 2.0

# === Apply smoothing ===
if ma_type_input != "None":
    df["CCI_MA"] = moving_average(df["CCI"], ma_length_input, ma_type_input, df["Volume"])

    # Bollinger Bands logic
    if ma_type_input == "SMA + Bollinger Bands":
        stdev = df["CCI"].rolling(ma_length_input).std() * bb_mult_input
        df["BB_upper"] = df["CCI_MA"] + stdev
        df["BB_lower"] = df["CCI_MA"] - stdev

print(df.tail(10))
