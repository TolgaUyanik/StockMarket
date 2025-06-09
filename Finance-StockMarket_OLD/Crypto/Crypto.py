import ccxt
import pandas as pd

# Create an instance of the Binance exchange
exchange = ccxt.binance()

# Define the symbol and timeframe
symbol = 'BTC/USDT'
timeframe = '1d'  # Daily timeframe

# Fetch OHLCV data (Open, High, Low, Close, Volume)
ohlcv = exchange.fetch_ohlcv(symbol, timeframe)

# Convert the OHLCV data into a DataFrame
df = pd.DataFrame(ohlcv, columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])

# Convert timestamp to datetime format
df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')

# Set the Timestamp column as the index
df.set_index('Timestamp', inplace=True)

# Print the DataFrame
print(df)

"""
bist = ["AEFES.IS", "AGHOL.IS", "AHGAZ.IS", "AKBNK.IS", "AKCNS.IS", "AKFGY.IS", "AKFYE.IS", "AKSA.IS",  "AKSEN.IS", "ALARK.IS", "ALBRK.IS", "ALFAS.IS", "ARCLK.IS", "ASELS.IS", "ASTOR.IS", "BERA.IS", "BIENY.IS",
        "BIMAS.IS", "BRSAN.IS", "BRYAT.IS", "BUCIM.IS", "CANTE.IS", "CCOLA.IS", "CIMSA.IS", "CWENE.IS", "DOAS.IS",  "DOHOL.IS", "ECILC.IS", "ECZYT.IS", "EGEEN.IS", "EKGYO.IS", "ENJSA.IS", "ENKAI.IS", "EREGL.IS",
        "EUPWR.IS", "EUREN.IS", "FROTO.IS", "GARAN.IS", "GENIL.IS", "GESAN.IS", "GLYHO.IS", "GUBRF.IS", "GWIND.IS", "HALKB.IS", "HEKTS.IS", "IMASM.IS", "IPEKE.IS", "ISCTR.IS", "ISDMR.IS", "ISGYO.IS", "ISMEN.IS",
        "IZMDC.IS", "KARSN.IS", "KAYSE.IS", "KCAER.IS", "KCHOL.IS", "KMPUR.IS", "KONTR.IS", "KONYA.IS", "KORDS.IS", "KOZAA.IS", "KOZAL.IS", "KRDMD.IS", "KZBGY.IS", "MAVI.IS",  "MGROS.IS", "MIATK.IS", "ODAS.IS",
        "OTKAR.IS", "OYAKC.IS", "PENTA.IS", "PETKM.IS", "PGSUS.IS", "PSGYO.IS", "QUAGR.IS", "SAHOL.IS", "SASA.IS",  "SISE.IS",  "SKBNK.IS", "SMRTG.IS", "SNGYO.IS", "SOKM.IS",  "TAVHL.IS", "TCELL.IS", "THYAO.IS",
        "TKFEN.IS", "TOASO.IS", "TSKB.IS",  "TTKOM.IS", "TTRAK.IS", "TUKAS.IS", "TUPRS.IS", "ULKER.IS", "VAKBN.IS", "VESBE.IS", "VESTL.IS", "YEOTK.IS", "YKBNK.IS", "YYLGD.IS", "ZOREN.IS"]

crypto = ["BTC-USD","ETH-USD","USDT-USD","SOL-USD","BNB-USD","STETH-USD","XRP-USD","USDC-USD","AVAX-USD","ADA-USD","DOGE-USD","SHIB-USD","DOT-USD","TON11419-USD","WTRX-USD","TRX-USD","LINK-USD","WBTC-USD",
          "MATIC-USD","BCH-USD","NEAR-USD","UNI7083-USD","LTC-USD","APT21794-USD","LEO-USD","ICP-USD","DAI-USD","RNDR-USD","FIL-USD","ATOM-USD","ETC-USD","TAO22974-USD","ARB11841-USD","IMX10603-USD","OKB-USD",
          "STX4847-USD","HBAR-USD","WHBAR-USD","GRT6719-USD","BTCB-USD","XLM-USD","INJ-USD","CRO-USD","OP-USD","WBETH-USD","KAS-USD","FDUSD-USD","THETA-USD","VET-USD","MKR-USD","PEPE24478-USD","RUNE-USD",
          "MNT27075-USD","WIF-USD","XMR-USD","FTM-USD","TIA22861-USD","SEI-USD","LDO-USD","AR-USD","FET-USD","RETH-USD","ALGO-USD","FLOW-USD","JUP29210-USD","SUI20947-USD","AAVE-USD","FLOKI-USD","GALA-USD",
          "BEAM28298-USD","EGLD-USD","BSV-USD","PYTH-USD","DYDX-USD","CFX-USD","BONK-USD","QNT-USD","AXS-USD","STRK22691-USD","SAND-USD","KCS-USD","WLD-USD","AGIX-USD","AKT-USD","ORDI-USD","MINA-USD","BTT-USD",
          "SNX-USD","MSOL-USD","XTZ-USD","BGB-USD","FLR-USD","APE18876-USD","ZBU-USD","CHZ-USD","MANA-USD","HNT-USD","TUSD-USD","USDE29470-USD","VBNB-USD"]

now = datetime.datetime.now()
stock_data = []
yuzde = 0
for stocks in crypto:
    ticker = yf.Ticker(stocks)
    stock_info = ticker.info
    data = {
    "Coin": stock_info["shortName"]
    "Opening": stock_info["open"],
    "Previous Close": stock_info["PreviousClose"]
    "52 Week Low": stock_info["fiftyTwoWeekLow"],
    "52 Week High": stock_info['fiftyTwoWeekHigh'],
    "Current Price": stock_info["currentPrice"],
    "Day Low": stock_info["dayLow"],
    "Day High": stock_info["dayHigh"],
    "Rec": stock_info["recommendationKey"]
    }
    #peg ratio not avaliable for each stocks 'fiftyDayAverage': 55341.09, 'twoHundredDayAverage': 40405.453
    
    print("%" + str(yuzde) +" "+ str(stocks))
    yuzde += 1
    stock_data.append(data)
    df = pd.DataFrame(stock_data)
    
df["change"] = ((df["Current Price"]/df["Opening"])-1)*100
df["Daily Change"] = ((df["Day High"]/df["Day Low"])-1)*100


buy_list =   df[df["Rec"]=="buy"]
hold_list  = df[df["Rec"]=="hold"]
sell_list  = df[df["Rec"]=="none"]
df["net_change"] = df["change"].abs()
change_list =df[df["net_change"]>=2]

buy_list = buy_list.sort_values(by="Price to Book", ascending=False)
hold_list= hold_list.sort_values(by="Price to Book", ascending=False)
sell_list= sell_list.sort_values(by="Price to Book", ascending=False)
pchange_list = change_list.sort_values(by="Price to Book",ascending=True)

buy_list.to_csv("buy_list.csv", index=False)
hold_list.to_csv("hold_list.csv", index=False)
sell_list.to_csv("sell_list.csv", index=False)
pchange_list.to_csv("Day_Trading.csv", index=False)

print("Change List")
print(pchange_list)
"""