# %1 differences exist but no worries about that.
import pandas as pd
import yfinance as yf

def calculate_sar_manually(dataframe, start=0.02, increment=0.02, maximum=0.2):
    """
    Manually calculates the Parabolic SAR without using a library function.
    
    Args:
        dataframe (pd.DataFrame): A DataFrame containing 'High' and 'Low' columns.
        start (float): The initial Acceleration Factor (AF).
        increment (float): The increment for the Acceleration Factor.
        maximum (float): The maximum value for the Acceleration Factor.
        
    Returns:
        pd.Series: A Series with the Parabolic SAR values.
    """
    sar_values = [0] * len(dataframe)
    
    # Initialize the SAR and Extreme Point (EP)
    # Start with a long trend (SAR below price)
    sar_values[0] = dataframe['Low'].iloc[0]
    ep = dataframe['High'].iloc[0]
    af = start
    is_long = True
    
    for i in range(1, len(dataframe)):
        current_sar = sar_values[i - 1]
        
        if is_long:
            # Calculate next SAR for a long trend
            new_sar = current_sar + af * (ep - current_sar)
            
            # Check for trend reversal
            if new_sar > dataframe['Low'].iloc[i]:
                is_long = False
                af = start
                sar_values[i] = ep
                ep = dataframe['Low'].iloc[i]
            else:
                sar_values[i] = new_sar
                # Update EP and AF if a new high is made
                if dataframe['High'].iloc[i] > ep:
                    ep = dataframe['High'].iloc[i]
                    af = min(maximum, af + increment)
        else: # Short trend
            # Calculate next SAR for a short trend
            new_sar = current_sar - af * (current_sar - ep)
            
            # Check for trend reversal
            if new_sar < dataframe['High'].iloc[i]:
                is_long = True
                af = start
                sar_values[i] = ep
                ep = dataframe['High'].iloc[i]
            else:
                sar_values[i] = new_sar
                # Update EP and AF if a new low is made
                if dataframe['Low'].iloc[i] < ep:
                    ep = dataframe['Low'].iloc[i]
                    af = min(maximum, af + increment)
    
    return pd.Series(sar_values, index=dataframe.index)

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
        
        # Pine Script Inputs
        start = 0.02
        increment = 0.02
        maximum = 0.2
        
        # 2. Calculate the Parabolic SAR manually
        sar_series = calculate_sar_manually(kchol_data, start, increment, maximum)
        
        # 3. Add the SAR values to the DataFrame
        kchol_data['SAR'] = sar_series
        
        # 4. Print the last 20 rows of the DataFrame to show the results
        print("\nDataFrame with Parabolic SAR values (last 20 rows):")
        print(kchol_data[['Close', 'SAR']].tail(20))

except Exception as e:
    print(f"An error occurred: {e}")