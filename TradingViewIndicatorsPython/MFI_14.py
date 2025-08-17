import pandas as pd
import pandas_ta as ta
import yfinance as yf

def calculate_mfi(dataframe, length=14):
    """
    Calculates the Money Flow Index (MFI).
    
    Args:
        dataframe (pd.DataFrame): A DataFrame containing 'High', 'Low', 'Close', and 'Volume' columns.
        length (int): The lookback period for the MFI calculation.
        
    Returns:
        pd.Series: A Series with the MFI values.
    """
    mfi_values = ta.mfi(
        high=dataframe['High'],
        low=dataframe['Low'],
        close=dataframe['Close'],
        volume=dataframe['Volume'],
        length=length
    )
    return mfi_values

# --- Main Script ---
# 1. Fetch historical data for KCHOL.IS from yfinance
#print("Fetching historical data for KCHOL.IS...")
try:
    stock_ticker = "KCHOL.IS"
    kchol_data = yf.download(stock_ticker, period="1y", interval="1d")
    
    if kchol_data.empty:
        print(f"No data found for the ticker: {stock_ticker}")
    else:
        # Check if the columns are a MultiIndex and flatten if they are
        if isinstance(kchol_data.columns, pd.MultiIndex):
            kchol_data.columns = kchol_data.columns.droplevel(1)
        
        # 2. Calculate the Money Flow Index (MFI)
        mfi_series = calculate_mfi(kchol_data)
        
        # 3. Add the MFI values to the DataFrame
        kchol_data['MFI'] = mfi_series
        
        # 4. Print the first few rows with valid MFI values
        print("\nDataFrame showing first valid MFI values:")
        # The MFI calculation will only have valid numbers after the lookback period.
        #print(kchol_data.dropna().head(20))
        
        # 5. Print the last 20 rows of the DataFrame
        print("\nDataFrame with MFI values (last 20 rows):")
        print(kchol_data.tail(20))

except Exception as e:
    print(f"An error occurred: {e}")