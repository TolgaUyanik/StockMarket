import pandas as pd
import pandas_ta as ta
import yfinance as yf

def calculate_roc(dataframe, length=9):
    """
    Calculates the Rate of Change (ROC) based on the Pine Script logic.
    
    Args:
        dataframe (pd.DataFrame): A DataFrame containing a 'Close' column.
        length (int): The lookback period for the ROC calculation.
        
    Returns:
        pd.Series: A Series with the ROC values.
    """
    # pandas_ta's roc function is a direct equivalent of the Pine Script formula.
    # It calculates 100 * (source - source[length]) / source[length]
    roc_values = ta.roc(
        close=dataframe['Close'],
        length=length
    )
    
    return roc_values

# --- Main Script ---
# 1. Fetch historical data for KCHOL.IS from yfinance
print("Fetching historical data for KCHOL.IS...")
try:
    stock_ticker = "KCHOL.IS"
    # Fetch data for the last year with daily intervals
    kchol_data = yf.download(stock_ticker, period="2mo", interval="1h")
    
    if kchol_data.empty:
        print(f"No data found for the ticker: {stock_ticker}")
    else:
        # Check if the columns are a MultiIndex and flatten if they are
        if isinstance(kchol_data.columns, pd.MultiIndex):
            kchol_data.columns = kchol_data.columns.droplevel(1)
        
        # 2. Calculate the Rate of Change (ROC)
        roc_series = calculate_roc(kchol_data)
        
        # 3. Add the ROC values to the DataFrame
        kchol_data['ROC'] = roc_series
        
        # 4. Print the last 20 rows of the DataFrame to show the results
        print("\nDataFrame with ROC values (last 20 rows):")
        print(kchol_data.tail(20))

except Exception as e:
    print(f"An error occurred: {e}")