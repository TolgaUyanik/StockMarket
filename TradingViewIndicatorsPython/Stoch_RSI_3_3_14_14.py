#It needs debug
import yfinance as yf
import pandas as pd
import numpy as np

def rsi_wilder(series, length):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    
    avg_gain = gain.ewm(alpha=1/length, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/length, adjust=False).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def stochastic_rsi(close, length_rsi=14, length_stoch=14, smooth_k=3, smooth_d=3):
    rsi = rsi_wilder(close, length_rsi)
    rsi_min = rsi.rolling(length_stoch).min()
    rsi_max = rsi.rolling(length_stoch).max()
    
    stoch_rsi = (rsi - rsi_min) / (rsi_max - rsi_min)
    
    k = stoch_rsi.ewm(span=smooth_k, adjust=False).mean()
    d = k.ewm(span=smooth_d, adjust=False).mean()

    # Make sure k and d have same index as close
    k = pd.Series(k, index=close.index)
    d = pd.Series(d, index=close.index)
    
    df = pd.DataFrame({
        "StochRSI_K": k * 100,
        "StochRSI_D": d * 100
    }, index=close.index)
    
    return df

if __name__ == "__main__":
    df = yf.download("KCHOL.IS", period="1y", interval="1d")
    close = df['Close']

    stoch_rsi_df = stochastic_rsi(close)

    print(stoch_rsi_df.tail(10))
