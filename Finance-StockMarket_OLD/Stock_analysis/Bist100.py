import yfinance as yf
import pandas as pd
import datetime

bist = ["AEFES.IS", "AGHOL.IS", "AHGAZ.IS", "AKBNK.IS", "AKCNS.IS", "AKFGY.IS", "AKFYE.IS", "AKSA.IS",  "AKSEN.IS", "ALARK.IS", "ALBRK.IS", "ALFAS.IS", "ARCLK.IS", "ASELS.IS", "ASTOR.IS", "BERA.IS", "BIENY.IS",
        "BIMAS.IS", "BRSAN.IS", "BRYAT.IS", "BUCIM.IS", "CANTE.IS", "CCOLA.IS", "CIMSA.IS", "CWENE.IS", "DOAS.IS",  "DOHOL.IS", "ECILC.IS", "ECZYT.IS", "EGEEN.IS", "EKGYO.IS", "ENJSA.IS", "ENKAI.IS", "EREGL.IS",
        "EUPWR.IS", "EUREN.IS", "FROTO.IS", "GARAN.IS", "GENIL.IS", "GESAN.IS", "GLYHO.IS", "GUBRF.IS", "GWIND.IS", "HALKB.IS", "HEKTS.IS", "IMASM.IS", "IPEKE.IS", "ISCTR.IS", "ISDMR.IS", "ISGYO.IS", "ISMEN.IS",
        "IZMDC.IS", "KARSN.IS", "KAYSE.IS", "KCAER.IS", "KCHOL.IS", "KMPUR.IS", "KONTR.IS", "KONYA.IS", "KORDS.IS", "KOZAA.IS", "KOZAL.IS", "KRDMD.IS", "KZBGY.IS", "MAVI.IS",  "MGROS.IS", "MIATK.IS", "ODAS.IS",
        "OTKAR.IS", "OYAKC.IS", "PENTA.IS", "PETKM.IS", "PGSUS.IS", "PSGYO.IS", "QUAGR.IS", "SAHOL.IS", "SASA.IS",  "SISE.IS",  "SKBNK.IS", "SMRTG.IS", "SNGYO.IS", "SOKM.IS",  "TAVHL.IS", "TCELL.IS", "THYAO.IS",
        "TKFEN.IS", "TOASO.IS", "TSKB.IS",  "TTKOM.IS", "TTRAK.IS", "TUKAS.IS", "TUPRS.IS", "ULKER.IS", "VAKBN.IS", "VESBE.IS", "VESTL.IS", "YEOTK.IS", "YKBNK.IS", "YYLGD.IS", "ZOREN.IS"]

now = datetime.datetime.now()
stock_data = []
yuzde = 0
for stocks in bist:
    ticker = yf.Ticker(stocks)
    stock_info = ticker.info
    data = {
    "Symbol": stock_info['symbol'],
    "Opening": stock_info["open"],
    "Price to Book": stock_info["priceToBook"],
    #"Book Value": stock_info["bookValue"],
    #"Previous Close": stock_info["previousClose"],
    "52 Week Low": stock_info["fiftyTwoWeekLow"],
    "52 Week High": stock_info['fiftyTwoWeekHigh'],
    "Current Price": stock_info["currentPrice"],
    "Day Low": stock_info["dayLow"],
    "Day High": stock_info["dayHigh"],
    "Rec": stock_info["recommendationKey"]
    }
    #peg ratio not avaliable for each stocks
    
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

buy_list.to_csv("Finance-StockMarket/Stock_analysis/buy_list.csv", index=False)
hold_list.to_csv("Finance-StockMarket/Stock_analysis/hold_list.csv", index=False)
sell_list.to_csv("Finance-StockMarket/Stock_analysis/sell_list.csv", index=False)
pchange_list.to_csv("Finance-StockMarket/Stock_analysis/Day_Trading.csv", index=False)

print("Change List")
print(pchange_list)
