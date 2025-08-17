import yfinance as yf
import pandas as pd
import numpy as np

def atr(df, length):
    high = df['High']
    low = df['Low']
    close = df['Close']
    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(length).mean()
    return atr
def supertrend(high, low, close, atr_length=10, factor=3.0):
    hl2 = (high + low) / 2
    atr_val = atr(high, low, close, atr_length)

    upperband = hl2 + factor * atr_val
    lowerband = hl2 - factor * atr_val

    supertrend = pd.Series(np.nan, index=close.index)
    direction = pd.Series(1, index=close.index)

    for i in range(atr_length, len(close)):
        curr_close = close.iat[i]
        prev_supertrend = supertrend.iat[i-1]
        prev_direction = direction.iat[i-1]
        curr_upper = upperband.iat[i]
        curr_lower = lowerband.iat[i]

        if pd.isna(prev_supertrend):
            supertrend.iat[i] = curr_lower
            direction.iat[i] = 1
            continue

        if curr_close > prev_supertrend:
            direction.iat[i] = 1
        elif curr_close < prev_supertrend:
            direction.iat[i] = -1
        else:
            direction.iat[i] = prev_direction

        if direction.iat[i] == 1:
            if prev_direction == 1:
                supertrend.iat[i] = max(curr_lower, prev_supertrend)
            else:
                supertrend.iat[i] = curr_lower
        else:
            if prev_direction == -1:
                supertrend.iat[i] = min(curr_upper, prev_supertrend)
            else:
                supertrend.iat[i] = curr_upper

    return supertrend, direction


def atr(high, low, close, length):
    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(length).mean()
    return atr


if __name__ == "__main__":
    df = yf.download("KCHOL.IS", period="1y", interval="1d")

    close = df['Close']['KCHOL.IS']
    high = df['High']['KCHOL.IS']
    low = df['Low']['KCHOL.IS']

    supertrend_vals, directions = supertrend(high, low, close, atr_length=10, factor=3.0)

    result = pd.DataFrame({
        "Supertrend": supertrend_vals,
        "Direction": directions
    }, index=close.index)

    print(result.tail(20))
