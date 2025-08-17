#Claude couldn't calculate it. Check again
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from datetime import datetime, timedelta

def calculate_volume_delta(data):
    """
    Calculate Volume Delta using price action approximation
    Since we don't have tick data, we approximate:
    - If close > open: assume most volume was buying (positive delta)
    - If close < open: assume most volume was selling (negative delta)
    - If close == open: delta is neutral (close to 0)
    """
    volume_delta = np.zeros(len(data))
    
    for i in range(len(data)):
        close_price = data['Close'].iloc[i]
        open_price = data['Open'].iloc[i]
        high_price = data['High'].iloc[i]
        low_price = data['Low'].iloc[i]
        volume = data['Volume'].iloc[i]
        
        if pd.isna(volume) or volume == 0:
            volume_delta[i] = 0
            continue
            
        # Calculate price range and close position within range
        price_range = high_price - low_price
        if price_range == 0:
            volume_delta[i] = 0
            continue
            
        # Calculate where close is relative to the range (0 = low, 1 = high)
        close_position = (close_price - low_price) / price_range
        
        # More sophisticated approximation using multiple factors
        # Factor 1: Close vs Open
        if close_price > open_price:
            co_factor = 0.6  # Bullish bias
        elif close_price < open_price:
            co_factor = -0.6  # Bearish bias
        else:
            co_factor = 0  # Neutral
            
        # Factor 2: Close position within the range
        # If close near high, more buying pressure
        # If close near low, more selling pressure
        range_factor = (close_position - 0.5) * 0.8
        
        # Combine factors and apply to volume
        net_factor = (co_factor + range_factor) / 2
        
        # Ensure factor stays within reasonable bounds
        net_factor = max(-1, min(1, net_factor))
        
        volume_delta[i] = volume * net_factor
    
    return pd.Series(volume_delta, index=data.index)

def create_volume_delta_ohlc(volume_delta):
    """
    Create OHLC-like data for volume delta to mimic Pine Script's plotcandle
    """
    # For volume delta "candles":
    # Open = previous close (or 0 for first bar)
    # High = max of open and close
    # Low = min of open and close  
    # Close = current volume delta
    
    vd_open = np.zeros(len(volume_delta))
    vd_high = np.zeros(len(volume_delta))
    vd_low = np.zeros(len(volume_delta))
    vd_close = volume_delta.values
    
    # First bar opens at 0
    vd_open[0] = 0
    
    for i in range(1, len(volume_delta)):
        vd_open[i] = vd_close[i-1]  # Open = previous close
        
    # Calculate high and low for each bar
    for i in range(len(volume_delta)):
        vd_high[i] = max(vd_open[i], vd_close[i])
        vd_low[i] = min(vd_open[i], vd_close[i])
        
        # Ensure high and low include 0 if the range crosses zero
        if vd_open[i] * vd_close[i] <= 0:  # If open and close have different signs or one is zero
            vd_high[i] = max(vd_high[i], 0)
            vd_low[i] = min(vd_low[i], 0)
    
    return {
        'open': pd.Series(vd_open, index=volume_delta.index),
        'high': pd.Series(vd_high, index=volume_delta.index),
        'low': pd.Series(vd_low, index=volume_delta.index),
        'close': volume_delta
    }

def plot_volume_delta(data, volume_delta, vd_ohlc):
    """
    Plot Volume Delta as candlestick-like bars
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), height_ratios=[2, 1])
    
    # Plot price chart on top
    ax1.plot(data.index, data['Close'], color='black', linewidth=1, label='Close Price')
    ax1.set_title('KCHOL.IS Stock Price')
    ax1.set_ylabel('Price (TRY)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot Volume Delta as bars on bottom
    
    # Create bar chart for volume delta
    colors = ['#008080' if val > 0 else '#FF0000' for val in volume_delta]
    bars = ax2.bar(range(len(volume_delta)), volume_delta, color=colors, alpha=0.8, width=0.8)
    
    # Add horizontal line at zero
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.7, linewidth=1)
    
    ax2.set_title('Volume Delta')
    ax2.set_ylabel('Volume Delta')
    ax2.set_xlabel('Date')
    ax2.grid(True, alpha=0.3)
    
    # Format x-axis to show fewer labels
    num_labels = min(10, len(data.index))
    step = max(1, len(data.index) // num_labels)
    ax2.set_xticks(range(0, len(data.index), step))
    ax2.set_xticklabels([data.index[i].strftime('%m-%d') for i in range(0, len(data.index), step)], 
                       rotation=45)
    
    plt.tight_layout()
    plt.show()

def get_data(symbol="KCHOL.IS", period="6mo"):
    """
    Fetch stock data from yfinance
    """
    ticker = yf.Ticker(symbol)
    data = ticker.history(period=period)
    return data

# Main execution
if __name__ == "__main__":
    # Fetch data
    print("Fetching KCHOL.IS data...")
    data = get_data("KCHOL.IS", period="6mo")
    
    if data.empty:
        print("No data found for KCHOL.IS")
        exit()
    
    # Check if volume data is available
    if data['Volume'].sum() == 0 or data['Volume'].isna().all():
        print("ERROR: The data vendor doesn't provide volume data for this symbol.")
        exit()
    
    print(f"Data fetched: {len(data)} rows from {data.index[0].date()} to {data.index[-1].date()}")
    print(f"Total volume traded: {data['Volume'].sum():,.0f}")
    
    # Calculate Volume Delta
    volume_delta = calculate_volume_delta(data)
    
    # Create OHLC-like structure for volume delta
    vd_ohlc = create_volume_delta_ohlc(volume_delta)
    
    # Plot the results
    plot_volume_delta(data, volume_delta, vd_ohlc)
    
    # Print recent values
    print("\nRecent Volume Delta values:")
    print("Date            Volume      Volume Delta")
    print("--------------------------------------")
    for i in range(-10, 0):
        date = data.index[i].strftime('%Y-%m-%d')
        volume = data['Volume'].iloc[i]
        vd = volume_delta.iloc[i]
        print(f"{date}      {volume:>8,.0f}      {vd:>8,.0f}")
    
    print(f"Current Volume: {data['Volume'].iloc[-1]:,.0f}")
    print(f"Current Volume Delta: {volume_delta.iloc[-1]:,.0f}")
    
    # Current signal
    current_vd = volume_delta.iloc[-1]
    if current_vd > 0:
        signal = "BULLISH (Buying pressure)"
    elif current_vd < 0:
        signal = "BEARISH (Selling pressure)"
    else:
        signal = "NEUTRAL (Balanced)"
    
    print(f"Signal: {signal}")