import yfinance as yf
import pandas as pd
import time 

stock_market = ["MSFT","AAPL","NVDA","AMZN","META","GOOGL","GOOG","BRK.B","LLY","AVGO","JPM","XOM","TSLA","UNH","V","PG","MA","JNJ","MRK","HD","COST","ABBV","CVX","CRM","BAC",
                "WMT","AMD","NFLX","PEP","KO","TMO","WFC","LIN","ADBE","DIS","MCD","CSCO","ACN","ABT","ORCL","QCOM","INTU","GE","CAT","VZ","AMAT","DHR","TXN","IBM","COP","CMCSA",
                "PM","INTC","UNP","NOW","AMGN","UBER","PFE","NEE","GS","AXP","RTX","SPGI","LOW","ISRG","HON","ELV","ETN","MU","PGR","BKNG","T","LRCX","C","MS","NKE","SYK","SCHW",
                "TJX","BSX","UPS","BLK","MDT","CI","DE","VRTX","ADP","LMT","CB","SBUX","MMC","ADI","BA","PLD","MDLZ","REGN","FI","KLAC","PANW","BMY","BX","TMUS","CMG","CVS","GILD",
                "SO","SNPS","AMT","EOG","WM","MO","CME","DUK","TGT","ICE","CDNS","CL","MPC","SHW","APH","MCK","ABNB","FCX","PH","ZTS","SLB","TDG","EQIX","NOC","PYPL","TT","ITW",
                "PSX","CSX","BDX","ANET","GD","PXD","USB","EMR","ORLY","PNC","HCA","FDX","NXPI","AON","CEG","MAR","MCO","PCAR","MSI","CTAS","ROP","VLO","ECL","COF","NSC","EW","DXCM",
                "GM","AIG","APD","WELL","HLT","F","AJG","AZO","MMM","TFC","CARR","NEM","MCHP","TRV","CPRT","WMB","OKE","URI","SPG","ADSK","KMB","AEP","SRE","ALL","OXY","ROST","O",
                "HES","AFL","MET","JCI","TEL","BK","DHI","NUE","DLR","IQV","D","STZ","GWW","FIS","AMP","LULU","AME","PSA","CCI","FTNT","IDXX","GIS","CNC","GEV","PRU","COR","A","YUM",
                "CMI","SMCI","DOW","RSG","LHX","MNST","PAYX","FAST","SYY","CTVA","HUM","LEN","OTIS","EXC","IR","PWR","FANG","MLM","CSGP","MSCI","KR","GEHC","PCG","KMI","KDP","ODFL",
                "MRNA","IT","HAL","ACGL","VMC","PEG","DVN","EL","CTSH","BKR","KVUE","CDW","ADM","ED","GPN","RCL","VRSK","DAL","ROK","DD","MPWR","DFS","DG","XYL","EA","KHC","PPG",
                "XEL","HIG","VICI","FICO","BIIB","WAB","TSCO","ON","ANSS","EXR","HSY","EFX","WST","EIX","RMD","AVB","FTV","MTD","EBAY","WTW","CHD","TRGP","KEYS","WEC","CBRE","CHTR",
                "CAH","DLTR","HWM","LYB","FITB","DOV","ZBH","NVR","HPQ","MTB","TROW","PHM","GLW","AWK","BR","WY","RJF","DTE","NDAQ","BLDR","ETR","TTWO","GPC","STT","IRM","WDC","EQR",
                "ALGN","GRMN","CPAY","HPE","AXON","HUBB","IFF","PTC","CTRA","SBAC","ES","NTAP","DECK","VLTO","BALL","MOH","BAX","STLD","ULTA","PPL","FE","STE","APTV","INVH","HBAN",
                "BRO","AEE","CBOE","OMC","TYL","ILMN","MKC","DRI","FSLR","CINF","CNP","SYF","WBD","CLX","ARE","WAT","RF","J","EXPE","COO","HOLX","PFG","TDY","LDOS","CMS","ATO","UAL",
                "AVY","VTR","TSN","NTRS","DPZ","STX","LH","LVS","IEX","TER","TXT","EQT","NRG","EXPD","SWKS","CFG","MRO","LUV","VRSN","FDS","ESS","WRB","EG","MAS","K","AKAM","PKG",
                "CCL","CF","CE","JBL","BG","DGX","ZBRA","CAG","MAA","TRMB","ENPH","BBY","POOL","SNA","NDSN","L","VTRS","KEY","SWK","EPAM","ALB","JBHT","HST","PNR","DOC","AMCR","LNT",
                "WBA","RVTY","LYV","ROL","KIM","JKHY","EVRG","LW","IPG","WRK","SJM","TAP","CRL","IP","GEN","UDR","MGM","LKQ","AES","PODD","EMN","NI","QRVO","JNPR","HII","KMX","ALLE",
                "FFIV","CPT","BBWI","HRL","AOS","CTLT","UHS","APA","MOS","TECH","TFX","REG","HSIC","INCY","WYNN","NWSA","AAL","AIZ","DAY","PAYC","TPR","CPB","BXP","BF.B","MTCH","SOLV",
                "GNRC","PNW","HAS","CHRW","CZR","ETSY","NCLH","FOXA","BWA","MKTX","FRT","RHI","FMC","DVA","BEN","CMA","RL","IVZ","GL","PARA","BIO","MHK","FOX","NWS"]

def market_analysis():
    stock_data = []
    yuzde = 1
    for stocks in stock_market:
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
        
        print(str(yuzde) +"/500 "+ str(stocks))
        yuzde += 1
        stock_data.append(data)
        df = pd.DataFrame(stock_data)
        


    df["change"]        =     ((df["Current Price"]/df["Opening"])-1)*100
    df["Daily Max Change"]  = ((df["Day High"]/df["Day Low"])-1)*100
    df['How Far Median'] =    ((df["Current Price"]/df["TMedian"])-1)*100
    df["How Far THigh"] =     ((df["THigh"]/df["Current Price"])-1)*100
    df["How Far TLow"]  =     ((df["Current Price"]/df["TLow"])-1)*100
    df["How Far TMean"] =     ((df["Current Price"]/df["TMean"])-1)*100
    df["Potantial"]     =     ((df["THigh"]-df["TMean"])/df["Current Price"])*100
    df["Under_Median"]  =     ((df["TMean"]-df["Current Price"])/df["TMean"])*100
#targetlara yüzde eklenecek yüzdeyle hesap kolaylaşır
#median - current price / current price gibi bir oran işimizi kolaylaştırır
    buy_list =   df[df["Rec"]=="buy"]
    hold_list  = df[df["Rec"]=="hold"]
    sell_list  = df[df["Rec"]=="none"]
    df["net_change"] = df["change"].abs()
    change_list =df[df["net_change"]>=1]

    trade_columns = ["Symbol","Price to Book","Potantial","Under_Median", "Current Price","THigh", 'TMedian', "TMean", "TLow", "change","52 Week High","52 Week Low" ]

    buy_list =           buy_list.sort_values(by="Price to Book", ascending=False)[trade_columns]
    hold_list=          hold_list.sort_values(by="Price to Book", ascending=False)[trade_columns]
    sell_list=          sell_list.sort_values(by="Price to Book", ascending=False)[trade_columns]
    pchange_list =    change_list.sort_values(by="change",ascending=True)[trade_columns]

    buy_list.to_csv("Finance-StockMarket/Stock_analysis/US_buy_list.csv", index=False)
    hold_list.to_csv("Finance-StockMarket/Stock_analysis/US_hold_list.csv", index=False)
    sell_list.to_csv("Finance-StockMarket/Stock_analysis/US_sell_list.csv", index=False)
    pchange_list.to_csv("Finance-StockMarket/Stock_analysis/US_Day_Trading.csv", index=False)

    print("Change List")
    print(pchange_list)

x = 0
market_analysis()