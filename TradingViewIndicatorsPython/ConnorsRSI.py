#It needs improvement but it can await. This is not a primary indicator for our analysis.
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def rsi(series, length):
    """
    Calculate RSI (Relative Strength Index)
    """
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(window=length).mean()
    avg_loss = loss.rolling(window=length).mean()
    
    # Use Wilder's smoothing method for more accurate RSI
    for i in range(length, len(series)):
        avg_gain.iloc[i] = (avg_gain.iloc[i-1] * (length-1) + gain.iloc[i]) / length
        avg_loss.iloc[i] = (avg_loss.iloc[i-1] * (length-1) + loss.iloc[i]) / length
    
    rs = avg_gain / avg_loss
    rsi_values = 100 - (100 / (1 + rs))
    
    return rsi_values

def updown(series):
    """
    Calculate consecutive up/down days counter
    """
    ud = np.zeros(len(series))
    
    for i in range(1, len(series)):
        if series.iloc[i] == series.iloc[i-1]:
            ud[i] = 0
        elif series.iloc[i] > series.iloc[i-1]:
            # Growing
            if i == 1 or ud[i-1] <= 0:
                ud[i] = 1
            else:
                ud[i] = ud[i-1] + 1
        else:
            # Declining
            if i == 1 or ud[i-1] >= 0:
                ud[i] = -1
            else:
                ud[i] = ud[i-1] - 1
    
    return pd.Series(ud, index=series.index)

def roc(series, length):
    """
    Calculate Rate of Change
    """
    return series.pct_change(periods=length) * 100

def percentrank(series, length):
    """
    Calculate percentile rank over a rolling window
    """
    def calc_percentrank(window):
        if len(window) < length:
            return np.nan
        current_value = window.iloc[-1]
        rank = (window < current_value).sum()
        return (rank / (len(window) - 1)) * 100
    
    return series.rolling(window=length).apply(calc_percentrank, raw=False)

def connors_rsi(data, lenrsi=3, lenupdown=2, lenroc=100):
    """
    Calculate Connors RSI
    """
    src = data['Close']
    
    # Calculate RSI
    rsi_values = rsi(src, lenrsi)
    
    # Calculate UpDown RSI
    updown_series = updown(src)
    updownrsi = rsi(updown_series, lenupdown)
    
    # Calculate ROC Percentrank
    roc_values = roc(src, 1)
    percentrank_values = percentrank(roc_values, lenroc)
    
    # Calculate Connors RSI as average of the three components
    crsi = (rsi_values + updownrsi + percentrank_values) / 3
    
    return crsi, rsi_values, updownrsi, percentrank_values

# Fetch KCHOL.IS data
def get_data(symbol="KCHOL.IS", period="1y"):
    """
    Fetch stock data from yfinance
    """
    ticker = yf.Ticker(symbol)
    data = ticker.history(period=period,interval = "1h")
    return data

# Main execution
if __name__ == "__main__":
    # Parameters (matching Pine Script defaults)
    lenrsi = 3
    lenupdown = 2
    lenroc = 100
    
    # Fetch data
    print("Fetching KCHOL.IS data...")
    data = get_data("KCHOL.IS", period="2mo")  # Using 2 years to have enough data for calculations
    
    if data.empty:
        print("No data found for KCHOL.IS")
        exit()
    
    print(f"Data fetched: {len(data)} rows from {data.index[0].date()} to {data.index[-1].date()}")
    
    # Calculate Connors RSI
    crsi, rsi_values, updownrsi, percentrank_values = connors_rsi(data, lenrsi, lenupdown, lenroc)
    
    # Create visualization
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Plot price
    ax1.plot(data.index, data['Close'], linewidth=1, label='KCHOL.IS Close Price')
    ax1.set_title('KCHOL.IS Stock Price')
    ax1.set_ylabel('Price (TRY)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot Connors RSI
    ax2.plot(data.index, crsi, color='#2962FF', linewidth=1.5, label='Connors RSI')
    ax2.axhline(y=70, color='#787B86', linestyle='-', alpha=0.7, label='Upper Band (70)')
    ax2.axhline(y=50, color='#787B86', linestyle='-', alpha=0.5, label='Middle Band (50)')
    ax2.axhline(y=30, color='#787B86', linestyle='-', alpha=0.7, label='Lower Band (30)')
    ax2.fill_between(data.index, 30, 70, color='lightblue', alpha=0.2, label='Background')
    
    ax2.set_title('Connors RSI')
    ax2.set_ylabel('CRSI Value')
    ax2.set_xlabel('Date')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 100)
    
    plt.tight_layout()
    plt.show()
    
    # Print recent values
    print("\nRecent Connors RSI values:")
    print("Date\t\tCRSI\tRSI\tUpDownRSI\tPercentRank")
    print("-" * 65)
    for i in range(-10, 0):  # Last 10 values
        date = data.index[i].strftime('%Y-%m-%d')
        crsi_val = crsi.iloc[i] if not pd.isna(crsi.iloc[i]) else "N/A"
        rsi_val = rsi_values.iloc[i] if not pd.isna(rsi_values.iloc[i]) else "N/A"
        updown_val = updownrsi.iloc[i] if not pd.isna(updownrsi.iloc[i]) else "N/A"
        percent_val = percentrank_values.iloc[i] if not pd.isna(percentrank_values.iloc[i]) else "N/A"
        
        if crsi_val != "N/A":
            print(f"{date}\t{crsi_val:.2f}\t{rsi_val:.2f}\t{updown_val:.2f}\t\t{percent_val:.2f}")
        else:
            print(f"{date}\t{crsi_val}\t{rsi_val}\t{updown_val}\t\t{percent_val}")
    
    # Calculate current signal
    current_crsi = crsi.iloc[-1]
    if not pd.isna(current_crsi):
        if current_crsi > 70:
            signal = "OVERBOUGHT"
        elif current_crsi < 30:
            signal = "OVERSOLD"
        else:
            signal = "NEUTRAL"
        
        print(f"\nCurrent Connors RSI: {current_crsi:.2f}")
        print(f"Signal: {signal}")
    else:
        print("\nCurrent Connors RSI: Not enough data")