#two point high from Tradingview but it seems good enoughly.
import numpy as np
import pandas as pd
import yfinance as yf

def rma(series, length):
    """Wilder's smoothing (RMA)"""
    alpha = 1 / length
    result = series.ewm(alpha=alpha, adjust=False).mean()
    return result

def adx(df, di_length=14, adx_length=14):
    high = df['High']
    low = df['Low']
    close = df['Close']

    up = high.diff()
    down = -low.diff()

    # flatten if needed
    up = up.values.flatten()
    down = down.values.flatten()

    plus_dm = np.where((up > down) & (up > 0), up, 0.0)
    minus_dm = np.where((down > up) & (down > 0), down, 0.0)

    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    tr_rma = rma(tr, di_length)
    plus_di = 100 * rma(pd.Series(plus_dm, index=df.index), di_length) / tr_rma
    minus_di = 100 * rma(pd.Series(minus_dm, index=df.index), di_length) / tr_rma

    sum_di = plus_di + minus_di
    diff_di = (plus_di - minus_di).abs()

    dx = 100 * diff_di / sum_di.replace(0, np.nan)
    adx = rma(dx.fillna(0), adx_length)

    return adx

# Example usage
df = yf.download("KCHOL.IS", period="6mo", interval="1h")

df['ADX_14'] = adx(df, di_length=14, adx_length=14)

print(df[['High', 'Low', 'Close', 'ADX_14']].tail(20))
