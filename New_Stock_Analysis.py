import yfinance as yf
import pandas as pd
import numpy as np
import os
from datetime import datetime

def calculate_rsi(data, period=14):
    """Calculates the Relative Strength Index (RSI) from scratch."""
    delta = data['Close'].diff(1)
    
    # Make a copy to avoid SettingWithCopyWarning
    gain = delta.copy()
    loss = delta.copy()
    
    gain[gain < 0] = 0
    loss[loss > 0] = 0
    
    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = abs(loss.rolling(window=period, min_periods=1).mean())
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(data, fast_period=12, slow_period=26, signal_period=9):
    """Calculates the Moving Average Convergence Divergence (MACD) from scratch."""
    ema_fast = data['Close'].ewm(span=fast_period, adjust=False).mean()
    ema_slow = data['Close'].ewm(span=slow_period, adjust=False).mean()
    
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    histogram = macd_line - signal_line
    
    return macd_line, signal_line, histogram

def calculate_cci(data, period=20):
    """Calculates the Commodity Channel Index (CCI) from scratch."""
    tp = (data['High'] + data['Low'] + data['Close']) / 3
    tp_sma = tp.rolling(window=period).mean()
    
    # Use a lambda function for mean deviation
    mean_dev = tp.rolling(window=period).apply(lambda x: np.mean(np.abs(x - x.mean())), raw=True)
    
    cci = (tp - tp_sma) / (0.015 * mean_dev)
    return cci

def calculate_adx(data, period=14):
    """
    Calculates the Average Directional Index (ADX) from scratch.
    This function now correctly returns a single Series.
    """
    df = data.copy()
    df['H-L'] = df['High'] - df['Low']
    df['H-PC'] = np.abs(df['High'] - df['Close'].shift(1))
    df['L-PC'] = np.abs(df['Low'] - df['Close'].shift(1))
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1)

    df['+DM'] = np.where((df['High'] - df['High'].shift(1)) > (df['Low'].shift(1) - df['Low']), df['High'] - df['High'].shift(1), 0)
    df['-DM'] = np.where((df['Low'].shift(1) - df['Low']) > (df['High'] - df['High'].shift(1)), df['Low'].shift(1) - df['Low'], 0)
    
    # Using Exponential Moving Average for smoothing
    atr = df['TR'].ewm(span=period, adjust=False).mean()
    plus_di = 100 * (df['+DM'].ewm(span=period, adjust=False).mean() / atr)
    minus_di = 100 * (df['-DM'].ewm(span=period, adjust=False).mean() / atr)
    
    dx = 100 * (np.abs(plus_di - minus_di) / (plus_di + minus_di))
    adx = dx.ewm(span=period, adjust=False).mean()
    
    # The crucial fix: return only the final ADX Series
    return adx

def calculate_ichimoku(data):
    """Calculates the Ichimoku Cloud components from scratch."""
    high = data['High']
    low = data['Low']

    # Tenkan-sen (Conversion Line)
    nine_period_high = high.rolling(window=9).max()
    nine_period_low = low.rolling(window=9).min()
    tenkan_sen = (nine_period_high + nine_period_low) / 2

    # Kijun-sen (Base Line)
    twenty_six_period_high = high.rolling(window=26).max()
    twenty_six_period_low = low.rolling(window=26).min()
    kijun_sen = (twenty_six_period_high + twenty_six_period_low) / 2

    # Senkou Span A (Leading Span A)
    senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(26)

    # Senkou Span B (Leading Span B)
    fifty_two_period_high = high.rolling(window=52).max()
    fifty_two_period_low = low.rolling(window=52).min()
    senkou_span_b = ((fifty_two_period_high + fifty_two_period_low) / 2).shift(26)

    return tenkan_sen, kijun_sen, senkou_span_a, senkou_span_b

def generate_trading_signals(data):
    """Generate basic trading signals based on the indicators."""
    signals = []
    latest = data.iloc[-1]
    
    # RSI Signals
    rsi_val = float(latest['RSI'])
    if rsi_val < 30:
        signals.append("RSI: OVERSOLD - Potential BUY signal")
    elif rsi_val > 70:
        signals.append("RSI: OVERBOUGHT - Potential SELL signal")
    else:
        signals.append(f"RSI: NEUTRAL ({rsi_val:.2f})")
    
    # MACD Signals
    macd_val = float(latest['MACD'])
    macd_signal = float(latest['MACD_Signal'])
    if macd_val > macd_signal:
        signals.append("MACD: BULLISH - MACD above signal line")
    else:
        signals.append("MACD: BEARISH - MACD below signal line")
    
    # CCI Signals
    cci_val = float(latest['CCI'])
    if cci_val > 100:
        signals.append("CCI: OVERBOUGHT - Potential SELL signal")
    elif cci_val < -100:
        signals.append("CCI: OVERSOLD - Potential BUY signal")
    else:
        signals.append(f"CCI: NEUTRAL ({cci_val:.2f})")
    
    # ADX Signals
    adx_val = float(latest['ADX'])
    if adx_val > 25:
        signals.append(f"ADX: STRONG TREND ({adx_val:.2f})")
    else:
        signals.append(f"ADX: WEAK TREND ({adx_val:.2f})")
    
    return signals

def analyze_stock(symbol, start_date, end_date, save_to_file=True):
    """
    Analyzes a stock by calculating key technical indicators from scratch.
    """
    try:
        print(f"Downloading data for {symbol}...")
        data = yf.download(symbol, start=start_date, end=end_date, auto_adjust=True)
        if data.empty:
            print(f"No data found for {symbol}. Please check the symbol or date range.")
            return None

        print("Calculating technical indicators...")
        # --- Calculate Indicators from Scratch ---
        data['RSI'] = calculate_rsi(data)
        data['MACD'], data['MACD_Signal'], data['MACD_Hist'] = calculate_macd(data)
        data['CCI'] = calculate_cci(data)
        data['ADX'] = calculate_adx(data)
        data['Tenkan-sen'], data['Kijun-sen'], data['Senkou_Span_A'], data['Senkou_Span_B'] = calculate_ichimoku(data)
        
        # Drop initial rows with NaN values to clean up the output
        clean_data = data.dropna()
        
        # Print results to console
        print("\n" + "="*60)
        print(f"TECHNICAL ANALYSIS RESULTS FOR {symbol.upper()}")
        print("="*60)
        
        # Latest values
        latest = clean_data.iloc[-1]
        print(f"\nLatest Close Price: ${float(latest['Close']):.2f}")
        print(f"Analysis Date: {latest.name.strftime('%Y-%m-%d')}")
        
        print(f"\nLatest Indicator Values:")
        print(f"RSI (14):           {float(latest['RSI']):.2f}")
        print(f"MACD:               {float(latest['MACD']):.4f}")
        print(f"MACD Signal:        {float(latest['MACD_Signal']):.4f}")
        print(f"MACD Histogram:     {float(latest['MACD_Hist']):.4f}")
        print(f"CCI (20):           {float(latest['CCI']):.2f}")
        print(f"ADX (14):           {float(latest['ADX']):.2f}")
        print(f"Tenkan-sen:         {float(latest['Tenkan-sen']):.2f}")
        print(f"Kijun-sen:          {float(latest['Kijun-sen']):.2f}")
        
        # Trading signals
        print(f"\nTRADING SIGNALS:")
        print("-" * 30)
        signals = generate_trading_signals(clean_data)
        for signal in signals:
            print(f"• {signal}")
        
        # Save to file if requested
        if save_to_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{symbol}_technical_analysis_{timestamp}.csv"
            clean_data.to_csv(filename)
            print(f"\nData saved to: {filename}")
            
            # Also save a summary report
            summary_filename = f"{symbol}_analysis_summary_{timestamp}.txt"
            with open(summary_filename, 'w') as f:
                f.write(f"TECHNICAL ANALYSIS SUMMARY FOR {symbol.upper()}\n")
                f.write("="*50 + "\n")
                f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Data Period: {start_date} to {end_date}\n")
                f.write(f"Latest Close Price: ${float(latest['Close']):.2f}\n\n")
                
                f.write("LATEST INDICATOR VALUES:\n")
                f.write(f"RSI (14):           {float(latest['RSI']):.2f}\n")
                f.write(f"MACD:               {float(latest['MACD']):.4f}\n")
                f.write(f"MACD Signal:        {float(latest['MACD_Signal']):.4f}\n")
                f.write(f"MACD Histogram:     {float(latest['MACD_Hist']):.4f}\n")
                f.write(f"CCI (20):           {float(latest['CCI']):.2f}\n")
                f.write(f"ADX (14):           {float(latest['ADX']):.2f}\n")
                f.write(f"Tenkan-sen:         {float(latest['Tenkan-sen']):.2f}\n")
                f.write(f"Kijun-sen:          {float(latest['Kijun-sen']):.2f}\n\n")
                
                f.write("TRADING SIGNALS:\n")
                for signal in signals:
                    f.write(f"• {signal}\n")
            
            print(f"Summary saved to: {summary_filename}")
        
        return clean_data
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # --- User Inputs ---
    stock_symbol = "KCHOL.IS"
    start_date = "2024-01-01"
    end_date = "2025-08-09"
    save_files = True  # Set to False if you don't want to save files
    # -------------------

    print("Starting Technical Analysis...")
    analysis_results = analyze_stock(stock_symbol, start_date, end_date, save_to_file=save_files)

    if analysis_results is not None:
        print(f"\nAnalysis completed successfully!")
        print(f"Total data points analyzed: {len(analysis_results)}")
        
        # Show last 5 days of data
        print(f"\nLast 5 days of data:")
        print(analysis_results[['Close', 'RSI', 'MACD', 'CCI', 'ADX']].tail().round(2))
    else:
        print("Analysis failed. Please check your inputs and try again.")

    print("\nDone!")