import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def ema(series, length):
    """
    Calculate Exponential Moving Average
    """
    return series.ewm(span=length, adjust=False).mean()

def sma(series, length):
    """
    Calculate Simple Moving Average
    """
    return series.rolling(window=length).mean()

def wma(series, length):
    """
    Calculate Weighted Moving Average
    """
    weights = np.arange(1, length + 1)
    return series.rolling(window=length).apply(
        lambda x: np.dot(x, weights) / weights.sum(), raw=True
    )

def rma(series, length):
    """
    Calculate Running Moving Average (SMMA)
    """
    alpha = 1.0 / length
    return series.ewm(alpha=alpha, adjust=False).mean()

def vwma(price_series, volume_series, length):
    """
    Calculate Volume Weighted Moving Average
    """
    pv = price_series * volume_series
    return pv.rolling(window=length).sum() / volume_series.rolling(window=length).sum()

def stdev(series, length):
    """
    Calculate Standard Deviation
    """
    return series.rolling(window=length).std()

def ma(source, length, ma_type, volume=None):
    """
    Universal Moving Average function
    """
    if ma_type == "SMA" or ma_type == "SMA + Bollinger Bands":
        return sma(source, length)
    elif ma_type == "EMA":
        return ema(source, length)
    elif ma_type == "SMMA (RMA)":
        return rma(source, length)
    elif ma_type == "WMA":
        return wma(source, length)
    elif ma_type == "VWMA":
        if volume is not None:
            return vwma(source, volume, length)
        else:
            # Fallback to SMA if volume not available
            return sma(source, length)
    else:
        return source

class EMAIndicator:
    def __init__(self, length=9, source='close', offset=0, 
                 ma_type="None", ma_length=14, bb_mult=2.0):
        self.length = length
        self.source = source
        self.offset = offset
        self.ma_type = ma_type
        self.ma_length = ma_length
        self.bb_mult = bb_mult
        self.enable_ma = ma_type != "None"
        self.is_bb = ma_type == "SMA + Bollinger Bands"
    
    def calculate(self, data):
        """
        Calculate EMA and smoothing MA if enabled
        """
        # Get source data
        if self.source == 'close':
            src = data['Close']
        elif self.source == 'open':
            src = data['Open']
        elif self.source == 'high':
            src = data['High']
        elif self.source == 'low':
            src = data['Low']
        else:
            src = data['Close']  # Default to close
        
        # Calculate main EMA
        main_ema = ema(src, self.length)
        
        # Apply offset if specified
        if self.offset != 0:
            main_ema = main_ema.shift(self.offset)
        
        # Calculate smoothing MA if enabled
        smoothing_ma = None
        smoothing_stdev = None
        bb_upper = None
        bb_lower = None
        
        if self.enable_ma:
            volume = data.get('Volume', None)
            smoothing_ma = ma(main_ema, self.ma_length, self.ma_type, volume)
            
            if self.is_bb:
                smoothing_stdev = stdev(main_ema, self.ma_length) * self.bb_mult
                bb_upper = smoothing_ma + smoothing_stdev
                bb_lower = smoothing_ma - smoothing_stdev
        
        return {
            'main_ema': main_ema,
            'smoothing_ma': smoothing_ma,
            'bb_upper': bb_upper,
            'bb_lower': bb_lower,
            'source': src
        }

def get_data(symbol="KCHOL.IS", period="2mo",interval="1h"):
    """
    Fetch stock data from yfinance
    """
    ticker = yf.Ticker(symbol)
    data = ticker.history(period=period,interval=interval)
    return data

def plot_ema(data, indicator_results):
    """
    Plot EMA indicator with price data
    """
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Plot price data (candlestick-like with lines)
    ax.plot(data.index, data['High'], color='lightgray', alpha=0.3, linewidth=0.5)
    ax.plot(data.index, data['Low'], color='lightgray', alpha=0.3, linewidth=0.5)
    ax.plot(data.index, data['Close'], color='black', linewidth=1, label='Close Price')
    
    # Plot main EMA
    ax.plot(data.index, indicator_results['main_ema'], 
            color='blue', linewidth=2, label=f'EMA({indicator.length})')
    
    # Plot smoothing MA if enabled
    if indicator_results['smoothing_ma'] is not None:
        ax.plot(data.index, indicator_results['smoothing_ma'], 
                color='orange', linewidth=1.5, label=f'EMA-based {indicator.ma_type}({indicator.ma_length})')
    
    # Plot Bollinger Bands if enabled
    if indicator_results['bb_upper'] is not None and indicator_results['bb_lower'] is not None:
        ax.plot(data.index, indicator_results['bb_upper'], 
                color='green', linewidth=1, alpha=0.7, label='Upper BB')
        ax.plot(data.index, indicator_results['bb_lower'], 
                color='green', linewidth=1, alpha=0.7, label='Lower BB')
        ax.fill_between(data.index, indicator_results['bb_upper'], indicator_results['bb_lower'],
                       color='green', alpha=0.1, label='BB Fill')
    
    ax.set_title('KCHOL.IS - EMA(9)')
    ax.set_ylabel('Price (TRY)')
    ax.set_xlabel('Date')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# Main execution
if __name__ == "__main__":
    # Fetch data
    print("Fetching KCHOL.IS data...")
    data = get_data("KCHOL.IS", period="2mo")
    
    if data.empty:
        print("No data found for KCHOL.IS")
        exit()
    
    print(f"Data fetched: {len(data)} rows from {data.index[0].date()} to {data.index[-1].date()}")
    
    # Basic EMA(9)
    indicator = EMAIndicator(length=9, source='close')
    results = indicator.calculate(data)
    plot_ema(data, results)
    
    # Print recent values
    print("Recent EMA(9) values:")
    print("Date\t\tClose\tEMA(9)")
    print("-" * 35)
    for i in range(-10, 0):
        date = data.index[i].strftime('%Y-%m-%d')
        close_val = data['Close'].iloc[i]
        ema_val = results['main_ema'].iloc[i]
        if not pd.isna(ema_val):
            print(f"{date}\t{close_val:.2f}\t{ema_val:.2f}")
    
    print(f"\nCurrent Close Price: {data['Close'].iloc[-1]:.2f} TRY")
    print(f"Current EMA(9): {results['main_ema'].iloc[-1]:.2f} TRY")
    
    # Signal analysis
    current_close = data['Close'].iloc[-1]
    current_ema = results['main_ema'].iloc[-1]
    
    if current_close > current_ema:
        signal = "BULLISH (Price above EMA)"
    elif current_close < current_ema:
        signal = "BEARISH (Price below EMA)"
    else:
        signal = "NEUTRAL (Price at EMA)"
    
    print(f"Signal: {signal}")