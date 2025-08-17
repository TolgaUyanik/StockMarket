# check_data.py
import yfinance as yf
import pandas_ta as ta
import pandas as pd

def run_sanity_check(symbol='AAPL'):
    """
    Fetches the latest OHLC data and calculates the RSI for a given stock symbol.
    This helps compare local calculations with a platform like TradingView.
    """
    print(f"--- Running Data Sanity Check for: {symbol} ---")
    
    try:
        # --- Step 1: Fetch Data from Yahoo Finance with different settings ---
        print("Trying different data fetch methods...")
        
        # Method 1: Standard fetch
        df1 = yf.download(symbol, period='3mo', interval='1d', progress=False, auto_adjust=False)
        
        # Method 2: With auto-adjust (handles splits/dividends)
        df2 = yf.download(symbol, period='3mo', interval='1d', progress=False, auto_adjust=True)
        
        # Method 3: Longer period to ensure enough data
        df3 = yf.download(symbol, period='1y', interval='1d', progress=False, auto_adjust=False)
        
        # Use the longest successful download
        df = df3 if not df3.empty else (df1 if not df1.empty else df2)
        
        if df.empty:
            print(f"No data downloaded for {symbol}. It might be an invalid ticker or there might be a network issue.")
            return
        
        # --- Fix for MultiIndex columns ---
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)
        df.columns = [str(col).strip() for col in df.columns]
        
        print(f"Data points available: {len(df)}")
        print(f"Date range: {df.index[0].date()} to {df.index[-1].date()}")
        
        # --- Step 2: Calculate RSI with multiple methods ---
        
        # Method 1: Standard pandas_ta RSI
        df.ta.rsi(length=14, append=True, talib=False)
        
        # Method 2: Try with TA-Lib if available
        try:
            df.ta.rsi(length=14, append=True, talib=True, suffix="TALib")
        except:
            print("TA-Lib not available, skipping TA-Lib RSI")
        
        # Method 3: Manual Wilder's smoothing (TradingView standard)
        close = df['Close']
        delta = close.diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        # Wilder's smoothing
        def wilders_smoothing(data, period):
            alpha = 1.0 / period
            result = pd.Series(index=data.index, dtype=float)
            # Start from period index to have enough data for initial SMA
            if len(data) < period:
                return result
            result.iloc[period-1] = data.iloc[:period].mean()  # Initial SMA
            for i in range(period, len(data)):
                result.iloc[i] = alpha * data.iloc[i] + (1 - alpha) * result.iloc[i-1]
            return result
        
        avg_gain_wilder = wilders_smoothing(gain, 14)
        avg_loss_wilder = wilders_smoothing(loss, 14)
        
        rs_wilder = avg_gain_wilder / avg_loss_wilder.replace(0, float('inf'))
        rsi_wilder = 100 - (100 / (1 + rs_wilder))
        df['RSI_Wilder'] = rsi_wilder
        
        # Method 4: Alternative Wilder's implementation
        # Sometimes the initial calculation differs
        def rsi_traditional(close_prices, period=14):
            delta = close_prices.diff()
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            
            # First calculation uses SMA
            avg_gain = gain.rolling(window=period).mean()
            avg_loss = loss.rolling(window=period).mean()
            
            # Subsequent calculations use Wilder's smoothing
            for i in range(period, len(close_prices)):
                avg_gain.iloc[i] = (avg_gain.iloc[i-1] * (period - 1) + gain.iloc[i]) / period
                avg_loss.iloc[i] = (avg_loss.iloc[i-1] * (period - 1) + loss.iloc[i]) / period
            
            rs = avg_gain / avg_loss.replace(0, float('inf'))
            rsi = 100 - (100 / (1 + rs))
            return rsi
        
        df['RSI_Traditional'] = rsi_traditional(close)
        
        # --- Step 3: Display results and debug info ---
        latest_data = df.iloc[-1]
        
        print(f"\nDate: {latest_data.name.date()}")
        print("--- OHLCV Data (from yfinance) ---")
        print(f"Open:   {latest_data['Open']:.2f}")
        print(f"High:   {latest_data['High']:.2f}")
        print(f"Low:    {latest_data['Low']:.2f}")
        print(f"Close:  {latest_data['Close']:.2f}")
        print(f"Volume: {latest_data['Volume']:.0f}")
        
        print("\n--- Indicator Values (Multiple Methods) ---")
        
        methods = [
            ('RSI_14', 'pandas_ta'),
            ('RSI_14TALib', 'TA-Lib'),
            ('RSI_Wilder', 'Wilder\'s'),
            ('RSI_Traditional', 'Traditional')
        ]
        
        for col, method in methods:
            if col in latest_data and pd.notna(latest_data[col]):
                print(f"RSI ({method}):      {latest_data[col]:.2f}")
        
        print(f"\nTradingView RSI: 39.39 (for comparison)")
        print("\n--- DEBUG: Last 5 days of price data ---")
        debug_data = df[['Close']].tail(5)
        for idx, row in debug_data.iterrows():
            print(f"{idx.date()}: Close = {row['Close']:.2f}")
        
        # Calculate price change over RSI period
        if len(df) >= 15:
            price_change = ((latest_data['Close'] - df['Close'].iloc[-15]) / df['Close'].iloc[-15]) * 100
            print(f"\nPrice change over last 14 days: {price_change:.2f}%")
            
        print("\n--- Possible Issues ---")
        print("1. Check if TradingView is using adjusted prices")
        print("2. Verify market timezone differences")
        print("3. Confirm TradingView's RSI period setting (should be 14)")
        print("4. Check if there are any stock splits or dividends affecting the data")
        
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    # You can change the stock symbol here to check any stock you want
    run_sanity_check('AAPL')