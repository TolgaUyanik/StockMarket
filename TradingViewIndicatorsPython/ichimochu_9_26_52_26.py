import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def add_ichimoku(df: pd.DataFrame, conversion_periods: int = 9, base_periods: int = 26, lagging_span_2_periods: int = 52, displacement: int = 26) -> pd.DataFrame:
    """
    Calculates and adds all Ichimoku Cloud components to a DataFrame.

    Args:
        df (pd.DataFrame): DataFrame with 'High', 'Low', and 'Close' columns.
        conversion_periods (int): The look-back period for the Conversion Line (Tenkan-sen).
        base_periods (int): The look-back period for the Base Line (Kijun-sen).
        lagging_span_2_periods (int): The look-back period for the Leading Span B (Senkou Span B).
        displacement (int): The displacement period for the Lagging Span (Chikou Span) and the Cloud.

    Returns:
        pd.DataFrame: The original DataFrame with Ichimoku components added.
    """
    # Donchian Channel calculation (midpoint of highest high and lowest low)
    high_9 = df['High'].rolling(window=conversion_periods).max()
    low_9 = df['Low'].rolling(window=conversion_periods).min()
    df['tenkan_sen'] = (high_9 + low_9) / 2 # Conversion Line

    high_26 = df['High'].rolling(window=base_periods).max()
    low_26 = df['Low'].rolling(window=base_periods).min()
    df['kijun_sen'] = (high_26 + low_26) / 2 # Base Line

    # --- Cloud (Kumo) ---
    # Leading Span A (Senkou Span A)
    df['senkou_span_a'] = ((df['tenkan_sen'] + df['kijun_sen']) / 2).shift(displacement)

    # Leading Span B (Senkou Span B)
    high_52 = df['High'].rolling(window=lagging_span_2_periods).max()
    low_52 = df['Low'].rolling(window=lagging_span_2_periods).min()
    df['senkou_span_b'] = ((high_52 + low_52) / 2).shift(displacement)

    # Lagging Span (Chikou Span)
    df['chikou_span'] = df['Close'].shift(-displacement)

    return df


# --- Main execution block ---
if __name__ == '__main__':
    # 1. Fetch Data
    ticker = 'KCHOL.IS'
    # The auto_adjust=True argument is now default and recommended.
    # It adjusts OHLC data for splits and dividends.
    data = yf.download(ticker, start='2025-05-01', interval='1h', auto_adjust=True)

    # 2. Calculate Ichimoku Indicators
    ichimoku_df = add_ichimoku(data.copy())

    # 3. Plotting
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(15, 8))

    # Plot Price
    ax.plot(ichimoku_df.index, ichimoku_df['Close'], color='lightgray', label='Close Price', linewidth=1)

    # Plot Ichimoku Lines
    ax.plot(ichimoku_df.index, ichimoku_df['tenkan_sen'], color='#2962FF', label='Conversion Line (Tenkan-sen)', linewidth=1.5)
    ax.plot(ichimoku_df.index, ichimoku_df['kijun_sen'], color='#B71C1C', label='Base Line (Kijun-sen)', linewidth=1.5)
    ax.plot(ichimoku_df.index, ichimoku_df['chikou_span'], color='#43A047', label='Lagging Span (Chikou)', linewidth=1.5, linestyle='--')
    
    # Plot Future Cloud (Kumo)
    ax.plot(ichimoku_df.index, ichimoku_df['senkou_span_a'], color='#A5D6A7', label='Leading Span A', linewidth=1)
    ax.plot(ichimoku_df.index, ichimoku_df['senkou_span_b'], color='#EF9A9A', label='Leading Span B', linewidth=1)

    # --- FIXED SECTION ---
    # Fill the Kumo Cloud using RGBA tuples for color
    # Green cloud for bullish Kumo
    ax.fill_between(ichimoku_df.index, ichimoku_df['senkou_span_a'], ichimoku_df['senkou_span_b'],
                    where=ichimoku_df['senkou_span_a'] >= ichimoku_df['senkou_span_b'],
                    color=(67/255, 160/255, 71/255, 0.5), interpolate=True)
    # Red cloud for bearish Kumo
    ax.fill_between(ichimoku_df.index, ichimoku_df['senkou_span_a'], ichimoku_df['senkou_span_b'],
                    where=ichimoku_df['senkou_span_a'] < ichimoku_df['senkou_span_b'],
                    color=(244/255, 67/255, 54/255, 0.5), interpolate=True)

    # --- Chart Styling ---
    ax.set_title(f'Ichimoku Cloud for {ticker}', fontsize=20)
    ax.set_ylabel('Price', fontsize=12)
    ax.set_xlabel('Date', fontsize=12)
    # Set x-axis limits to show the future cloud
    ax.set_xlim(ichimoku_df.index.min(), ichimoku_df.index.max() + pd.DateOffset(days=5))
    ax.legend(loc='upper left')
    ax.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.show()