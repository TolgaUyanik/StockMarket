import yfinance as yf
import pandas as pd
import time 

bist = ["AEFES.IS", "AKBNK.IS",  "AKFYE.IS","ARCLK.IS", "ASELS.IS", "ASTOR.IS",
        "BIMAS.IS", "BRSAN.IS", "BRYAT.IS", "BUCIM.IS", "CANTE.IS", "CCOLA.IS", "CIMSA.IS", "CWENE.IS", "DOAS.IS",  "DOHOL.IS", "ECILC.IS", "ECZYT.IS", "EGEEN.IS", "EKGYO.IS", "ENJSA.IS", "ENKAI.IS", "EREGL.IS",
        "EUPWR.IS", "EUREN.IS", "FROTO.IS", "GARAN.IS", "GENIL.IS", "GESAN.IS", "GLYHO.IS", "GUBRF.IS", "GWIND.IS", "HALKB.IS", "HEKTS.IS", "IMASM.IS", "IPEKE.IS", "ISCTR.IS", "ISDMR.IS", "ISGYO.IS", "ISMEN.IS",
        "IZMDC.IS", "KARSN.IS", "KAYSE.IS", "KCAER.IS", "KCHOL.IS", "KMPUR.IS", "KONTR.IS", "KONYA.IS", "KORDS.IS", "KOZAA.IS", "KOZAL.IS", "KRDMD.IS", "KZBGY.IS", "MAVI.IS",  "MGROS.IS", "MIATK.IS", "ODAS.IS",
        "OTKAR.IS", "OYAKC.IS", "PENTA.IS", "PETKM.IS", "PGSUS.IS", "PSGYO.IS", "QUAGR.IS", "SAHOL.IS", "SASA.IS",  "SISE.IS",  "SKBNK.IS", "SMRTG.IS", "SNGYO.IS", "SOKM.IS",  "TAVHL.IS", "TCELL.IS", "THYAO.IS",
        "TKFEN.IS", "TOASO.IS", "TSKB.IS",  "TTKOM.IS", "TTRAK.IS", "TUKAS.IS", "TUPRS.IS", "ULKER.IS", "VAKBN.IS", "VESBE.IS", "VESTL.IS", "YEOTK.IS", "YKBNK.IS", "YYLGD.IS", "ZOREN.IS"]

def market_analysis():
    stock_data = []
    yuzde = 1
    for stocks in bist:
        ticker = yf.Ticker(stocks)
        stock_info = ticker.info
        data = {
            "Symbol": stock_info.get('symbol', None),
            "Price to Book": stock_info.get("priceToBook", None),
            "Current Price": stock_info.get("currentPrice", None),
            "THigh": stock_info.get('targetHighPrice', None),
            "TLow": stock_info.get('targetLowPrice', None),
            "TMean": stock_info.get('targetMeanPrice', None),
            "TMedian": stock_info.get('targetMedianPrice', None),
            "Book Value": stock_info.get("bookValue", None),
            "52 Week Low": stock_info.get("fiftyTwoWeekLow", None),
            "52 Week High": stock_info.get('fiftyTwoWeekHigh', None),
            "Opening": stock_info.get("open", None),
            "Day Low": stock_info.get("dayLow", None),
            "Day High": stock_info.get("dayHigh", None),    
            "Rec": stock_info.get("recommendationKey", None),
            #"PegRatio": stock_info.get('trailingPegRatio', None),
        }
        
        print("%" + str(yuzde) +" "+ str(stocks))
        yuzde += 1
        stock_data.append(data)
        df = pd.DataFrame(stock_data)
        


    df["change"]        =     ((df["Current Price"]/df["Opening"])-1)*100
    df["Daily Max Change"]  = ((df["Day High"]/df["Day Low"])-1)*100
    #df['How Far Median'] =    ((df["Current Price"]/df["TMedian"])-1)*100
    #df["How Far THigh"] =     ((df["THigh"]/df["Current Price"])-1)*100
    #df["How Far TLow"]  =     ((df["Current Price"]/df["TLow"])-1)*100
    #df["How Far TMean"] =     ((df["Current Price"]/df["TMean"])-1)*100
    df["How Far High"] = ((df["Current Price"]/df["52 Week High"]))
    df["How Far Low"]  = ((df["52 Week Low"]/df["Current Price"]))

    buy_list =   df[df["Rec"]=="buy"]
    hold_list  = df[df["Rec"]=="hold"]
    sell_list  = df[df["Rec"]=="none"]
    df["net_change"] = df["change"].abs()
    change_list =df[df["net_change"]>=2]

    trade_columns = ["Symbol","Price to Book","Current Price", "change", "52 Week Low","52 Week High","How Far High", "How Far Low"]

    buy_list =           buy_list.sort_values(by="Price to Book", ascending=False)[trade_columns]
    hold_list=          hold_list.sort_values(by="Price to Book", ascending=False)[trade_columns]
    sell_list=          sell_list.sort_values(by="Price to Book", ascending=False)[trade_columns]
    pchange_list =    change_list.sort_values(by="change",ascending=True)[trade_columns]

    buy_list.to_csv("Finance-StockMarket/Stock_analysis/buy_list.csv", index=False)
    hold_list.to_csv("Finance-StockMarket/Stock_analysis/hold_list.csv", index=False)
    sell_list.to_csv("Finance-StockMarket/Stock_analysis/sell_list.csv", index=False)
    pchange_list.to_csv("Finance-StockMarket/Stock_analysis/Day_Trading.csv", index=False)

    print("Change List")
    print(pchange_list)

x = 0
market_analysis()
    
#BIST 100'de Target kısmında uyumsuz olan şirketler var onları düşürmem gerekiyor
#YFinance Targetları nasıl hesaplıyor? Bu hesaplamaya göre ciddi bir strateji oluşturulabilir
