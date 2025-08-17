import pandas as pd
import numpy as np
import yfinance as yf
pd.set_option("display.float_format", "{:,.2f}".format)

# === Download KCHOL.IS data ===
df = yf.download("KCHOL.IS", period="6mo", interval="1d")

# Flatten multi-level column names if they exist
if isinstance(df.columns, pd.MultiIndex):
    df.columns = ['_'.join(col).strip() for col in df.columns.values]

# Ensure Volume column exists
vol_col = [col for col in df.columns if "Volume" in col][0]  # detect correct volume column

# Fill NaN volumes with 0 and check if all zero
if df[vol_col].fillna(0).sum().item() == 0:
    raise ValueError("No volume is provided by the data vendor.")

# === 1. Accumulation/Distribution Line (ADL) ===
def accumulation_distribution_line(high, low, close, volume):
    mfm = ((close - low) - (high - close)) / (high - low)  # Money Flow Multiplier
    mfm = mfm.replace([np.inf, -np.inf], 0).fillna(0)      # Handle divide-by-zero
    mfv = mfm * volume                                    # Money Flow Volume
    return mfv.cumsum()                                   # ADL (cumulative sum)

df["ADL"] = accumulation_distribution_line(
    df[[col for col in df.columns if "High" in col][0]],
    df[[col for col in df.columns if "Low" in col][0]],
    df[[col for col in df.columns if "Close" in col][0]],
    df[vol_col].fillna(0)
)

# === 2. EMA function ===
def ema(series, length):
    return series.ewm(span=length, adjust=False).mean()

# === 3. Chaikin Oscillator ===
short = 3
long = 10
df["Chaikin_Osc"] = ema(df["ADL"], short) - ema(df["ADL"], long)

print(df[["ADL", "Chaikin_Osc"]].tail(10))
