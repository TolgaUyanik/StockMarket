import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
List_of_anomali = []
List_of_anomali1 = []
bist = ["AEFES.IS", "AGHOL.IS", "AHGAZ.IS", "AKBNK.IS", "AKCNS.IS", "AKFGY.IS", "AKFYE.IS", "AKSA.IS",  "AKSEN.IS", "ALARK.IS", "ALBRK.IS", "ALFAS.IS", "ARCLK.IS", "ASELS.IS", "ASTOR.IS", "BERA.IS", "BIENY.IS",
        "BIMAS.IS", "BRSAN.IS", "BRYAT.IS", "BUCIM.IS", "CANTE.IS", "CCOLA.IS", "CIMSA.IS", "CWENE.IS", "DOAS.IS",  "DOHOL.IS", "ECILC.IS", "ECZYT.IS", "EGEEN.IS", "EKGYO.IS", "ENJSA.IS", "ENKAI.IS", "EREGL.IS",
        "EUPWR.IS", "EUREN.IS", "FROTO.IS", "GARAN.IS", "GENIL.IS", "GESAN.IS", "GLYHO.IS", "GUBRF.IS", "GWIND.IS", "HALKB.IS", "HEKTS.IS", "IMASM.IS", "IPEKE.IS", "ISCTR.IS", "ISDMR.IS", "ISGYO.IS", "ISMEN.IS",
        "IZMDC.IS", "KARSN.IS", "KAYSE.IS", "KCAER.IS", "KCHOL.IS", "KMPUR.IS", "KONTR.IS", "KONYA.IS", "KORDS.IS", "KOZAA.IS", "KOZAL.IS", "KRDMD.IS", "KZBGY.IS", "MAVI.IS",  "MGROS.IS", "MIATK.IS", "ODAS.IS",
        "OTKAR.IS", "OYAKC.IS", "PENTA.IS", "PETKM.IS", "PGSUS.IS", "PSGYO.IS", "QUAGR.IS", "SAHOL.IS", "SASA.IS",  "SISE.IS",  "SKBNK.IS", "SMRTG.IS", "SNGYO.IS", "SOKM.IS",  "TAVHL.IS", "TCELL.IS", "THYAO.IS",
        "TKFEN.IS", "TOASO.IS", "TSKB.IS",  "TTKOM.IS", "TTRAK.IS", "TUKAS.IS", "TUPRS.IS", "ULKER.IS", "VAKBN.IS", "VESBE.IS", "VESTL.IS", "YEOTK.IS", "YKBNK.IS", "YYLGD.IS", "ZOREN.IS"]
"""
df = yf.download("KCHOL.IS", period="3d", interval="1d")
df1 = (df["Adj Close"])
df1 = df1.to_frame().reset_index(drop=False)
#0-24
print(df1)
"""

for stocks in bist:
    df = yf.download(stocks, period="3d", interval="1h")
    df1 = (df["Adj Close"])
    df1.reset_index(drop=True, inplace=True)
    print(df1)
    try:
        x = df1.loc[0]
    except:
        pass
    try:
        y= df1.loc[8]
    except:
        pass
    try:
        z= df1.loc[16]
    except:
        pass
    yesterday = ((y/x)-1)*100
    today     = ((z/y)-1)*100
    if abs(today) > 3 :
        List_of_anomali.append(stocks)
        List_of_anomali.append(today)
    elif abs(yesterday) > 3:
        List_of_anomali1.append(stocks)
        List_of_anomali1.append(yesterday)
    else:
        pass
    
print("Yesterday")
print(List_of_anomali1)
print("Today")
print(List_of_anomali)

