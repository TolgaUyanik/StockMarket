#It includes SMA_on_SMA. It needs a check
import pandas as pd
import yfinance as yf

# --- Manual Moving Average Functions ---

def sma(series, length):
    """Calculates the Simple Moving Average (SMA) manually."""
    return series.rolling(window=length).mean()

def ema(series, length):
    """Calculates the Exponential Moving Average (EMA) manually."""
    return series.ewm(span=length, adjust=False).mean()

def rma(series, length):
    """Calculates the Relative Moving Average (RMA) manually (equivalent to Wilders Smoothing)."""
    alpha = 1 / length
    return series.ewm(alpha=alpha, adjust=False).mean()

def wma(series, length):
    """Calculates the Weighted Moving Average (WMA) manually."""
    weights = pd.Series(range(1, length + 1))
    def wma_calc(x):
        return (x * weights).sum() / weights.sum()
    return series.rolling(window=length).apply(wma_calc, raw=True)

def vwma(dataframe, length):
    """Calculates the Volume Weighted Moving Average (VWMA) manually."""
    vwap = (dataframe['Close'] * dataframe['Volume']).rolling(window=length).sum() / dataframe['Volume'].rolling(window=length).sum()
    return vwap

def stdev(series, length):
    """Calculates the standard deviation manually."""
    return series.rolling(window=length).std()

# --- Main Script ---
# 1. Fetch historical data for KCHOL.IS from yfinance
print("Fetching historical data for KCHOL.IS...")
try:
    stock_ticker = "KCHOL.IS"
    kchol_data = yf.download(stock_ticker, period="1y", interval="1d")
    
    if kchol_data.empty:
        print(f"No data found for the ticker: {stock_ticker}")
    else:
        # Check if the columns are a MultiIndex and flatten if they are
        if isinstance(kchol_data.columns, pd.MultiIndex):
            kchol_data.columns = kchol_data.columns.droplevel(1)
        
        # Pine Script Inputs
        len = 9
        maTypeInput = "SMA"  # Change this to any option to test: "SMA", "EMA", "RMA", "WMA", "VWMA"
        maLengthInput = 14
        bbMultInput = 2.0
        
        # 2. Calculate the primary SMA
        kchol_data['SMA'] = sma(kchol_data['Close'], len)
        
        # 3. Calculate the Smoothing Moving Average (applied to the primary SMA)
        ma_func = {
            "SMA": sma,
            "EMA": ema,
            "RMA": rma,
            "WMA": wma,
            "VWMA": vwma
        }
        
        enableMA = maTypeInput != "None"
        isBB = maTypeInput == "SMA + Bollinger Bands"
        
        if enableMA:
            # Note: VWMA uses the original data, others use the SMA series
            if maTypeInput == "VWMA":
                smoothingMA = vwma(kchol_data, maLengthInput)
            else:
                smoothingMA = ma_func.get(maTypeInput.split(" ")[0], sma)(kchol_data['SMA'], maLengthInput)
            
            kchol_data[f'{maTypeInput}_on_SMA'] = smoothingMA
            
            if isBB:
                # Calculate Bollinger Bands on the smoothing MA
                smoothingStDev = stdev(kchol_data['SMA'], maLengthInput) * bbMultInput
                kchol_data['BB_Upper'] = smoothingMA + smoothingStDev
                kchol_data['BB_Lower'] = smoothingMA - smoothingStDev

        # 4. Print the last 20 rows of the DataFrame
        print("\nDataFrame with Moving Averages (last 20 rows):")
        print(kchol_data.tail(20))

except Exception as e:
    print(f"An error occurred: {e}")