import yfinance as yf
import pandas as pd

# XU100.IS Stocks 
bist = ["AEFES.IS", "AGHOL.IS", "AHGAZ.IS", "AKBNK.IS", "AKCNS.IS", "AKFGY.IS", "AKFYE.IS", "AKSA.IS",  "AKSEN.IS", "ALARK.IS", "ALBRK.IS", "ALFAS.IS", "ARCLK.IS", "ASELS.IS", "ASTOR.IS", "BERA.IS", "BIENY.IS",
        "BIMAS.IS", "BRSAN.IS", "BRYAT.IS", "BUCIM.IS", "CANTE.IS", "CCOLA.IS", "CIMSA.IS", "CWENE.IS", "DOAS.IS",  "DOHOL.IS", "ECILC.IS", "ECZYT.IS", "EGEEN.IS", "ENJSA.IS", "ENKAI.IS", "EREGL.IS",
        "EUPWR.IS", "EUREN.IS", "FROTO.IS", "GARAN.IS", "GENIL.IS", "GESAN.IS", "GLYHO.IS", "GUBRF.IS", "GWIND.IS", "HALKB.IS", "HEKTS.IS", "IMASM.IS", "IPEKE.IS", "ISCTR.IS", "ISDMR.IS", "ISMEN.IS",
        "IZMDC.IS", "KARSN.IS", "KAYSE.IS", "KCAER.IS", "KCHOL.IS", "KMPUR.IS", "KONTR.IS", "KONYA.IS", "KORDS.IS", "KOZAA.IS", "KOZAL.IS", "KRDMD.IS", "KZBGY.IS", "MAVI.IS",  "MGROS.IS", "MIATK.IS", "ODAS.IS",
        "OTKAR.IS", "OYAKC.IS", "PENTA.IS", "PETKM.IS", "PGSUS.IS", "QUAGR.IS", "SAHOL.IS", "SASA.IS",  "SISE.IS",  "SKBNK.IS", "SMRTG.IS", "SOKM.IS",  "TAVHL.IS", "TCELL.IS", "THYAO.IS",
        "TKFEN.IS", "TOASO.IS", "TSKB.IS",  "TTKOM.IS", "TTRAK.IS", "TUKAS.IS", "TUPRS.IS", "ULKER.IS", "VAKBN.IS", "VESBE.IS", "VESTL.IS", "YEOTK.IS", "YKBNK.IS", "YYLGD.IS", "ZOREN.IS"]
def market_analysis():
    stock_data = []
    per = 1
    for stocks in bist:
        ticker = yf.Ticker(stocks)
        stock_info = ticker.info
        data = {key: stock_info.get(key, None) for key in ["symbol", "priceToBook", "currentPrice", "targetHighPrice", "targetLowPrice", "targetMeanPrice","targetMedianPrice",
                                                            "bookValue", "fiftyTwoWeekLow", "fiftyTwoWeekHigh", "open", "dayLow", "dayHigh", "recommendationKey"]}
        print("%" + str(per) +" "+ str(stocks))
        per += 1
        stock_data.append(data)
        df = pd.DataFrame(stock_data)
        
    df["change"]        =           ((df["currentPrice"]/df["open"])-1)*100
    df["net_change"] =                df["change"].abs()
    df["Daily Max Change"]  =       ((df["dayHigh"]/df["dayLow"])-1)*100
    df['How Far Median'] =          ((df["currentPrice"]/df["targetMedianPrice"])-1)*100
    df["How Far targetHighPrice"] = ((df["targetHighPrice"]/df["currentPrice"])-1)*100
    df["How Far targetLowPrice"]  = ((df["currentPrice"]/df["targetLowPrice"])-1)*100
    df["How Far targetMeanPrice"] = ((df["currentPrice"]/df["targetMeanPrice"])-1)*100
    df["Potantial"]     =           ((df["targetHighPrice"]-df["targetMeanPrice"])/df["currentPrice"])*100
    df["Under_Median"]  =           ((df["targetMeanPrice"]-df["currentPrice"])/df["targetMeanPrice"])*100
    df["How Close targetLowPrice"]= ((df["targetMeanPrice"]-df["targetLowPrice"])/df["currentPrice"])*100

#Recommendation Based Stock Listing    
    buy_list =    df[df["recommendationKey"]=="buy"]
    hold_list  =  df[df["recommendationKey"]=="hold"]
    sell_list  =  df[df["recommendationKey"]=="none"]
    change_list = df[df["net_change"]>=1]

    trade_columns = ["symbol","priceToBook","Potantial","Under_Median","How Close targetLowPrice", "currentPrice","targetHighPrice", 'targetMedianPrice', "targetMeanPrice", "targetLowPrice", "change","fiftyTwoWeekHigh","fiftyTwoWeekLow" ]

    buy_list =     buy_list.sort_values(by="priceToBook", ascending=False)[trade_columns]
    hold_list=     hold_list.sort_values(by="priceToBook", ascending=False)[trade_columns]
    sell_list=     sell_list.sort_values(by="priceToBook", ascending=False)[trade_columns]
    pchange_list = change_list.sort_values(by="change",ascending=True)[trade_columns]

    buy_list.to_csv("Stock_analysis/buy_list.csv", index=False)
    hold_list.to_csv("Stock_analysis/hold_list.csv", index=False)
    sell_list.to_csv("Stock_analysis/sell_list.csv", index=False)
    pchange_list.to_csv("Stock_analysis/Day_Trading.csv", index=False)

    print("Change List")
    print(pchange_list)

x = 0
market_analysis()