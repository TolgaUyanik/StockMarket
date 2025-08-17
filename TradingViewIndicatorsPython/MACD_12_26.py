import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def add_macd(df: pd.DataFrame, fast_length: int = 12, slow_length: int = 26, signal_length: int = 9, source_col: str = 'Close', osc_ma_type: str = 'EMA', sig_ma_type: str = 'EMA') -> pd.DataFrame:
    """
    Calculates and adds MACD components to a DataFrame based on Pine Script logic.

    Args:
        df (pd.DataFrame): DataFrame with source data.
        fast_length (int): The look-back period for the fast MA.
        slow_length (int): The look-back period for the slow MA.
        signal_length (int): The look-back period for the signal line MA.
        source_col (str): The column to use for calculation (e.g., 'Close').
        osc_ma_type (str): Type of MA for oscillator ('SMA' or 'EMA').
        sig_ma_type (str): Type of MA for signal line ('SMA' or 'EMA').

    Returns:
        pd.DataFrame: The original DataFrame with MACD components added.
    """
    # Calculate Fast MA
    if osc_ma_type == 'SMA':
        fast_ma = df[source_col].rolling(window=fast_length).mean()
    else:
        fast_ma = df[source_col].ewm(span=fast_length, adjust=False).mean()

    # Calculate Slow MA
    if osc_ma_type == 'SMA':
        slow_ma = df[source_col].rolling(window=slow_length).mean()
    else:
        slow_ma = df[source_col].ewm(span=slow_length, adjust=False).mean()

    # Calculate MACD Line
    df['macd'] = fast_ma - slow_ma

    # Calculate Signal Line
    if sig_ma_type == 'SMA':
        df['signal'] = df['macd'].rolling(window=signal_length).mean()
    else:
        df['signal'] = df['macd'].ewm(span=signal_length, adjust=False).mean()

    # Calculate Histogram
    df['hist'] = df['macd'] - df['signal']

    return df

# --- Main execution block ---
if __name__ == '__main__':
    # 1. Fetch Data
    ticker = 'KCHOL.IS'
    data = yf.download(ticker, start='2025-06-01', interval='1h', auto_adjust=True)

    # 2. Calculate MACD Indicators
    macd_df = add_macd(data.copy())

    # 3. Plotting
    plt.style.use('dark_background')
    # Create two subplots: one for price, one for MACD
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), sharex=True, gridspec_kw={'height_ratios': [2, 1]})

    # --- Plot 1: Price ---
    ax1.plot(macd_df.index, macd_df['Close'], color='lightgray', label='Close Price')
    ax1.set_title(f'{ticker} Price and MACD', fontsize=20)
    ax1.set_ylabel('Price', fontsize=12)
    ax1.legend(loc='upper left')
    ax1.grid(True, linestyle='--', alpha=0.3)

    # --- Plot 2: MACD ---
    # Plot MACD and Signal lines
    ax2.plot(macd_df.index, macd_df['macd'], color='#2962FF', label='MACD', linewidth=1.5)
    ax2.plot(macd_df.index, macd_df['signal'], color='#FF6D00', label='Signal', linewidth=1.5)
    ax2.axhline(0, color='#787B86', linestyle='--', linewidth=1) # Zero Line

    # --- Conditional Histogram Coloring (Replicating Pine Script logic) ---
    hist_prev = macd_df['hist'].shift(1)
    
    # Condition 1: Green (hist >= 0 and rising)
    rising_green = (macd_df['hist'] >= 0) & (macd_df['hist'] > hist_prev)
    ax2.bar(macd_df.index[rising_green], macd_df['hist'][rising_green], color='#26A69A', label='Rising')

    # Condition 2: Light Green (hist >= 0 and falling)
    falling_light_green = (macd_df['hist'] >= 0) & (macd_df['hist'] <= hist_prev)
    ax2.bar(macd_df.index[falling_light_green], macd_df['hist'][falling_light_green], color='#B2DFDB')

    # Condition 3: Red (hist < 0 and falling)
    falling_red = (macd_df['hist'] < 0) & (macd_df['hist'] < hist_prev)
    ax2.bar(macd_df.index[falling_red], macd_df['hist'][falling_red], color='#FF5252', label='Falling')

    # Condition 4: Light Red (hist < 0 and rising)
    rising_light_red = (macd_df['hist'] < 0) & (macd_df['hist'] >= hist_prev)
    ax2.bar(macd_df.index[rising_light_red], macd_df['hist'][rising_light_red], color='#FFCDD2')
    
    # --- Chart Styling ---
    ax2.set_ylabel('MACD', fontsize=12)
    ax2.set_xlabel('Date', fontsize=12)
    # Create a custom legend for the histogram colors
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='#26A69A', label='Histogram (Rising, >0)'),
                       Patch(facecolor='#B2DFDB', label='Histogram (Falling, >0)'),
                       Patch(facecolor='#FF5252', label='Histogram (Falling, <0)'),
                       Patch(facecolor='#FFCDD2', label='Histogram (Rising, <0)'),
                       plt.Line2D([0], [0], color='#2962FF', lw=2, label='MACD'),
                       plt.Line2D([0], [0], color='#FF6D00', lw=2, label='Signal')]
    ax2.legend(handles=legend_elements, loc='upper left')
    ax2.grid(True, linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    plt.show()