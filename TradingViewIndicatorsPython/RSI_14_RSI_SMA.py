import pandas as pd
import pandas_ta as ta
import yfinance as yf

# --- Main Script ---
# 1. Fetch historical data from yfinance
print("Fetching historical data for KCHOL.IS...")
try:
    stock_ticker = "KCHOL.IS"
    # Fetch data for the last year with daily intervals
    kchol_data = yf.download(stock_ticker, period="1y", interval="1d")
    
    if kchol_data.empty:
        print(f"No data found for the ticker: {stock_ticker}")
    else:
        # Check if the columns are a MultiIndex and flatten if they are
        if isinstance(kchol_data.columns, pd.MultiIndex):
            kchol_data.columns = kchol_data.columns.droplevel(1)
        
        # Pine Script Inputs
        rsiLengthInput = 14
        maTypeInput = "SMA"  # Options: "None", "SMA", "EMA", "RMA", "WMA", "VWMA"
        maLengthInput = 14
        bbMultInput = 2.0
        
        # 2. Calculate the Relative Strength Index (RSI)
        # pandas_ta.rsi is a direct equivalent of the standard RSI calculation.
        kchol_data['RSI'] = ta.rsi(kchol_data['Close'], length=rsiLengthInput)
        
        # 3. Calculate the Smoothing Moving Average
        # This replicates the 'ma' function and switch statement from the Pine Script
        ma_func = {
            "SMA": ta.sma,
            "EMA": ta.ema,
            "RMA": ta.rma,  # pandas_ta's rma is equivalent to Pine Script's SMMA
            "WMA": ta.wma,
            "VWMA": ta.vwma
        }
        
        if maTypeInput in ma_func:
            smoothing_ma = ma_func[maTypeInput](kchol_data['RSI'], length=maLengthInput)
            kchol_data[f'{maTypeInput}_{maLengthInput}_RSI'] = smoothing_ma
            
            # If Bollinger Bands are enabled, calculate them
            if maTypeInput == "SMA" and maTypeInput == "SMA + Bollinger Bands":
                stdev = ta.stdev(kchol_data['RSI'], length=maLengthInput)
                kchol_data['BB_Upper'] = smoothing_ma + stdev * bbMultInput
                kchol_data['BB_Lower'] = smoothing_ma - stdev * bbMultInput
        
        # 4. Print the last 20 rows of the DataFrame to show the results
        print("\nDataFrame with RSI and Smoothing MA values (last 20 rows):")
        print(kchol_data.tail(20))

except Exception as e:
    print(f"An error occurred: {e}")