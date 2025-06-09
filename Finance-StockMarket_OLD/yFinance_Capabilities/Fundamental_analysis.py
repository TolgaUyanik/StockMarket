import yfinance as yf
import pandas as pd


bist = ["AEFES.IS", "AGHOL.IS", "AHGAZ.IS", "AKBNK.IS", "AKCNS.IS", "AKFGY.IS", "AKFYE.IS", "AKSA.IS",  "AKSEN.IS", "ALARK.IS", "ALBRK.IS", "ALFAS.IS", "ARCLK.IS", "ASELS.IS", "ASTOR.IS", "BERA.IS", "BIENY.IS",
        "BIMAS.IS", "BRSAN.IS", "BRYAT.IS", "BUCIM.IS", "CANTE.IS", "CCOLA.IS", "CIMSA.IS", "CWENE.IS", "DOAS.IS",  "DOHOL.IS", "ECILC.IS", "ECZYT.IS", "EGEEN.IS", "EKGYO.IS", "ENJSA.IS", "ENKAI.IS", "EREGL.IS",
        "EUPWR.IS", "EUREN.IS", "FROTO.IS", "GARAN.IS", "GENIL.IS", "GESAN.IS", "GLYHO.IS", "GUBRF.IS", "GWIND.IS", "HALKB.IS", "HEKTS.IS", "IMASM.IS", "IPEKE.IS", "ISCTR.IS", "ISDMR.IS", "ISGYO.IS", "ISMEN.IS",
        "IZMDC.IS", "KARSN.IS", "KAYSE.IS", "KCAER.IS", "KCHOL.IS", "KMPUR.IS", "KONTR.IS", "KONYA.IS", "KORDS.IS", "KOZAA.IS", "KOZAL.IS", "KRDMD.IS", "KZBGY.IS", "MAVI.IS",  "MGROS.IS", "MIATK.IS", "ODAS.IS",
        "OTKAR.IS", "OYAKC.IS", "PENTA.IS", "PETKM.IS", "PGSUS.IS", "PSGYO.IS", "QUAGR.IS", "SAHOL.IS", "SASA.IS",  "SISE.IS",  "SKBNK.IS", "SMRTG.IS", "SNGYO.IS", "SOKM.IS",  "TAVHL.IS", "TCELL.IS", "THYAO.IS",
        "TKFEN.IS", "TOASO.IS", "TSKB.IS",  "TTKOM.IS", "TTRAK.IS", "TUKAS.IS", "TUPRS.IS", "ULKER.IS", "VAKBN.IS", "VESBE.IS", "VESTL.IS", "YEOTK.IS", "YKBNK.IS", "YYLGD.IS", "ZOREN.IS"]
shorttrade= ["Shorttrade"]
longtrade = ["Longtrade"]
speculation_decetor =["There is a spek"]


for stocks in bist:
    ticker = yf.Ticker(stocks)
    stock_info = ticker.info
    previousClose =   stock_info["previousClose"]
    opening =         stock_info["open"] 
    bookValue =       stock_info["bookValue"]
    pricetoBook =     stock_info["priceToBook"]
    fiftytwoweeklow = stock_info["fiftyTwoWeekLow"]
    currentPrice =    stock_info["currentPrice"]
    dayLow  =         stock_info["dayLow"]
    dayHigh =         stock_info["dayHigh"]    
#    targetLowPrice  = stock_info["targetLowPrice"]
#    targetHighPrice = stock_info["targetHighPrice"]
    
    print(stocks)
#    print(targetLowPrice)
#    print(targetHighPrice)

    speculation = ((dayHigh/dayLow)-1)*100
    change= ((currentPrice/opening)-1)*100

    if abs(change) > 2:
        shorttrade.append(stocks)
        shorttrade.append(change)     
    else:
        pass

    if abs(speculation) > 6:
        speculation_decetor.append(stocks)
        speculation_decetor.append(speculation) 



    if pricetoBook < 1:
        longtrade.append(stocks)
        longtrade.append(pricetoBook)
#price to book needs an improvement
#book value and market mean is important
#for longtrade value of book must be different market mean value
#targetHighPrice and targetLowPrice is important
            
#defter değerini hesaplarken şirketleri kendi içerisinde gruplandırmak gerekiyor bunu bist30 için farklı bir kod olarak yazabilirim
#Ayrı bir dosyaya ihtiyacım var ve bunları sektör sektör ayırmam gerekiyor P/B ratio 1den küçükler iyi bir göstergeyken bunları test etmem aşırı önemli        

print(shorttrade)
print(longtrade)
print(speculation_decetor)



#target price important
#price analysis 52 week mean value can be guide us
#price to sales ratio will compare market mean value
#Price to book ratio will compare market mean value
#Json haline getirilecek
#xbank gibi liste oluşturup oranın en düşük defter değerine sahip olan 5 veya 10 şirketini yazdırabilirim