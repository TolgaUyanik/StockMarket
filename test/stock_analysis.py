import yfinance as yf
import pandas as pd
import numpy as np
import pandas_ta as ta
from datetime import datetime

def classic_analysis(bist):
    stock_dict = {}
    stock_data = []
    stock_number = 0
    for stocks in bist:
        try:
            ticker = yf.Ticker(stocks)
            stock_info = ticker.info
            data = {key: stock_info.get(key, None) for key in ["symbol", "priceToBook", "currentPrice", "targetHighPrice", "targetLowPrice", "targetMeanPrice", "targetMedianPrice",
                                                                "bookValue", "open", "dayLow", "dayHigh", "recommendationKey", 'fiftyTwoWeekLow', 'fiftyTwoWeekHigh']}
            historical_data = ticker.history(period="1y")  # Get historical data for the stock
            stock_dict[stocks] = historical_data
            if historical_data.empty:
                print(f"No historical data for {stocks}, skipping...")
                continue  # Skip this ticker if no historical data is found
            stock_number = 1 + stock_number
            print(f"\r{stock_number}/{len(bist)} Downloaded {stocks} data", end='', flush=True)

            historical_data['RSI'] = ta.rsi(historical_data['Close'], length=14)  # Calculate RSI (Relative Strength Index)
            adx_data = ta.adx(historical_data['High'], historical_data['Low'], historical_data['Close'], length=14)  # Calculate ADX (Average Directional Index)
            historical_data['ADX'] = adx_data['ADX_14']
            macd = ta.macd(historical_data['Close'], fast=12, slow=26, signal=9)
            historical_data = pd.concat([historical_data, macd], axis=1)
            
            historical_data['MACDAS'] = historical_data['MACD_12_26_9'] - historical_data['MACDs_12_26_9']
            historical_data['MACDAS_Signal'] = historical_data['MACDAS'].ewm(span=9, adjust=False).mean()
            historical_data['CCI'] = ta.cci(historical_data['High'], historical_data['Low'], historical_data['Close'], length=20)  # Calculate CCI (Commodity Channel Index)
            historical_data['ROC'] = ta.roc(historical_data['Close'], length=12)  # Calculate ROC (Rate of Change)
            historical_data['ATR'] = ta.atr(historical_data['High'], historical_data['Low'], historical_data['Close'], length=14)  # Calculate ATR (Average True Range)
            historical_data['MFI'] = ta.mfi(historical_data['High'], historical_data['Low'], historical_data['Close'], historical_data['Volume'], length=14)
            historical_data["FWMA"]= ta.fwma(historical_data['Close'],length=14)
            historical_data['OBV'] = ta.obv(historical_data['Close'], historical_data['Volume'])  # Calculate OBV (On-Balance Volume)
            historical_data['CMF'] = ta.cmf(historical_data['High'], historical_data['Low'], historical_data['Close'], historical_data['Volume'])# Calculate CMF (Chaikin Money Flow)
            historical_data['AD'] =  ta.ad(historical_data['High'], historical_data['Low'], historical_data['Close'], historical_data['Volume'])  # Calculate A/D Line (Accumulation/Distribution Line)
            historical_data["VWAP"]= ta.vwap(historical_data['High'], historical_data['Low'], historical_data['Close'], historical_data['Volume'])
            historical_data["kama"]= ta.kama(historical_data['Close'],length=14) # lenght
            supertrend = ta.supertrend(historical_data['High'], historical_data['Low'], historical_data['Close'], length=10, multiplier=3)
            historical_data['Supertrend'] = supertrend['SUPERT_10_3.0']
            historical_data['Supertrend_direction'] = supertrend['SUPERTd_10_3.0']
            
            # Calculate Ichimoku Cloud
            ichimoku = ta.ichimoku(historical_data['High'], historical_data['Low'], historical_data['Close'], 
                                 tenkan=9, kijun=26, senkou=52)
            historical_data['Ichimoku_Tenkan'] = ichimoku['ITS_9']
            historical_data['Ichimoku_Kijun'] = ichimoku['IKS_26']
            historical_data['Ichimoku_Senkou_A'] = ichimoku['ISA_9']
            historical_data['Ichimoku_Senkou_B'] = ichimoku['ISB_26']
            historical_data['Ichimoku_Chikou'] = ichimoku['ICS_26']
            
            # Calculate Stochastic Oscillator
            stoch = ta.stoch(historical_data['High'], historical_data['Low'], historical_data['Close'], k=14, d=3)
            historical_data['Stoch_K'] = stoch['STOCHk_14_3_3']
            historical_data['Stoch_D'] = stoch['STOCHd_14_3_3']
            
            # Calculate Stochastic RSI
            stochrsi = ta.stochrsi(historical_data['Close'], length=14, rsi_length=14, k=3, d=3)
            historical_data['StochRSI_K'] = stochrsi['STOCHRSIk_14_14_3_3']
            historical_data['StochRSI_D'] = stochrsi['STOCHRSId_14_14_3_3']
 
            # Calculate Bollinger Bands
            bollinger = ta.bbands(historical_data['Close'], length=20, std=2)
            historical_data['BB_Middle'] = bollinger.iloc[:, 1]  # Middle Band
            historical_data['BB_Upper'] = bollinger.iloc[:, 2]  # Upper Band
            historical_data['BB_Lower'] = bollinger.iloc[:, 0]  # Lower Band
            historical_data['BB_BWidth'] = bollinger.iloc[:, 3]  # Bandwidth
            historical_data['BB_%B'] = bollinger.iloc[:, 4]  # %B

            data.update({"RSI": historical_data['RSI'].iloc[-1], "ADX": historical_data['ADX'].iloc[-1],"CCI": historical_data['CCI'].iloc[-1], "ROC": historical_data['ROC'].iloc[-1], "ATR": historical_data['ATR'].iloc[-1], "OBV": historical_data['OBV'].iloc[-1],
                        "CMF": historical_data['CMF'].iloc[-1], "AD": historical_data['AD'].iloc[-1], "MFI": historical_data['MFI'].iloc[-1],
                        "MACD": historical_data['MACD_12_26_9'].iloc[-1],"MACD_signal": historical_data['MACDs_12_26_9'].iloc[-1],"MACD_Hist": historical_data['MACDh_12_26_9'].iloc[-1],"MACDAS": historical_data['MACDAS'].iloc[-1],"MACDAS_Signal": historical_data['MACDAS_Signal'].iloc[-1],
                        "BB_Middle": historical_data['BB_Middle'].iloc[-1],"BB_Upper": historical_data['BB_Upper'].iloc[-1],"BB_Lower": historical_data['BB_Lower'].iloc[-1],'BB_%B': historical_data['BB_%B'].iloc[-1],'BB_BWidth': historical_data['BB_BWidth'].iloc[-1],
                        "FWMA": historical_data["FWMA"].iloc[-1],"VWAP": historical_data["VWAP"].iloc[-1],
                        "kama" : historical_data["kama"].iloc[-1],
                        "Supertrend": historical_data['Supertrend'].iloc[-1],
                        "Supertrend_direction": historical_data['Supertrend_direction'].iloc[-1],
                        "Stoch_K": historical_data['Stoch_K'].iloc[-1],
                        "Stoch_D": historical_data['Stoch_D'].iloc[-1],
                        "StochRSI_K": historical_data['StochRSI_K'].iloc[-1],
                        "StochRSI_D": historical_data['StochRSI_D'].iloc[-1],
                        "Ichimoku_Tenkan": historical_data['Ichimoku_Tenkan'].iloc[-1],
                        "Ichimoku_Kijun": historical_data['Ichimoku_Kijun'].iloc[-1],
                        "Ichimoku_Senkou_A": historical_data['Ichimoku_Senkou_A'].iloc[-1],
                        "Ichimoku_Senkou_B": historical_data['Ichimoku_Senkou_B'].iloc[-1],
                        "Ichimoku_Chikou": historical_data['Ichimoku_Chikou'].iloc[-1],
                        })
            stock_data.append(data)

        except Exception as e:
            print(f"Error fetching data for {stocks}: {e}")

    # Create a DataFrame from the stock data
    df = pd.DataFrame(stock_data)
    df["YF%"] = ((df["currentPrice"] - df["fiftyTwoWeekLow"])/(df["fiftyTwoWeekHigh"]-df["currentPrice"]))*100 #Check the differences
    df["MACDAS-dif"] = df["MACDAS"] - df["MACDAS_Signal"] 
    df["change"] = ((df["currentPrice"] / df["open"]) - 1) * 100
    df["BB_Pot"] = ((df['BB_Upper'] / df["currentPrice"]) - 1) * 100
    df["BB_Opt"] = ((df['BB_Lower'] / df["currentPrice"]) - 1) * 100
    df["TrendWay"] = np.select([(df["ADX"] > 20) & (df["ROC"] > 0), (df["ADX"] > 20) & (df["ROC"] <= 0), (df["ADX"] <= 20)], ["upper", "lower", "no-trend"], default="unknown")

    df1 = df[["symbol", "Stoch_K","Stoch_D","StochRSI_K","StochRSI_D","Supertrend","Supertrend_direction","kama","MACDAS-dif","MACDAS","MACDAS_Signal", 'BB_BWidth', 'BB_%B',"YF%","MFI", "OBV", "RSI","AD", "ADX", "CCI", "ROC","CMF", "ATR","FWMA","VWAP", "currentPrice","change",
              "Ichimoku_Tenkan", "Ichimoku_Kijun", "Ichimoku_Senkou_A", "Ichimoku_Senkou_B", "Ichimoku_Chikou"]]
    df2 = df1.rename(columns={"currentPrice": "CPrice"})

    pd.set_option('display.float_format', '{:.2f}'.format)
    print("\nDownload process is done!")
    df2
    now = datetime.now()  # This part will copy for our sell lists. Especially further analysis.
    formatted_time = now.strftime("%m-%d_%H-%M-%S")
    df2.to_csv(f"CSVs/Results/{formatted_time}.csv")
    df2.to_csv(f"CSVs/Results last.csv")
    print(df2)
    return df2 