import pandas as pd
import numpy as np
import yfinance as yf

# Show normal numbers instead of scientific notation
pd.set_option("display.float_format", "{:,.6f}".format)

# Download KCHOL.IS data
df = yf.download("KCHOL.IS", period="6mo", interval="1d")

# Flatten multi-level columns if present
if isinstance(df.columns, pd.MultiIndex):
    df.columns = ['_'.join(filter(None, col)).strip() for col in df.columns.values]

# Check volume validity
vol_col = [col for col in df.columns if "Volume" in col][0]
if df[vol_col].fillna(0).sum() == 0:
    raise ValueError("No volume is provided by the data vendor.")

length = 20  # CMF length

# Flatten data to 1D arrays
close = df[[col for col in df.columns if "Close" in col][0]].to_numpy().flatten()
high = df[[col for col in df.columns if "High" in col][0]].to_numpy().flatten()
low = df[[col for col in df.columns if "Low" in col][0]].to_numpy().flatten()
volume = df[vol_col].to_numpy().flatten()

# Calculate Money Flow Multiplier × Volume (AD part)
ad = np.where(
    ((close == high) & (close == low)) | (high == low),
    0,
    ((2 * close - low - high) / (high - low)) * volume
).flatten()

# CMF calculation
sum_ad = pd.Series(ad).rolling(window=length).sum()
sum_vol = pd.Series(volume).rolling(window=length).sum()
cmf = sum_ad / sum_vol

# Save CMF to DataFrame
df["CMF"] = cmf.values  # align indices

# Show last 10 rows of Close and CMF
close_col = [col for col in df.columns if "Close" in col][0]
print(df[[close_col, "CMF"]].dropna().tail(10))
