
import yfinance as yf, pandas as pd, matplotlib.pyplot as plt, pandas_ta as ta, numpy as np
import time
import os, math, time, warnings
from datetime import datetime, timedelta
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=FutureWarning)
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', None)        # Don't wrap columns
pd.set_option('display.max_colwidth', None) # Show full content of each column
pd.set_option('display.float_format', lambda x: '%.2f' % x)

endeks = ['XU100.IS', 'XU030.IS','^GSPC', '^IXIC', '^DJI', '^GDAXI', '^FTSE', '^N225', '^HSI','GC=F', 'SI=F', 'PL=F', 'PA=F','BTC-USD', 'ETH-USD', 'USDT-USD','CL=F', 'NG=F', 'ZC=F', 'ZS=F', 'CT=F','USDTRY=X', 'EURUSD=X', 'GBPUSD=X', 'JPY=X','^TNX', '^TYX','^VIX']
sectors = ["XU100.IS","XU030.IS","XUSIN.IS","XBANK.IS"] #These stocks are not working in yfinance library "XU050.IS","XSGRT.IS","XTRZM.IS","XFINAN.IS","XSGRT.IS","XTEKS.IS","XGIDA.IS","XILTM.IS","XMESY.IS","XKAGT.IS","XKMYA.IS","XTAST.IS","XULAS.IS","XTCRT.IS","XMANA.IS","XELKT.IS","XUTEK.IS","XBLSM.IS","XHOLD.IS",]
nasdaq = ["AAPL", "MSFT", "AMZN", "GOOGL", "GOOG", "META", "NVDA", "TSLA", "PEP", "AVGO", "COST", "CSCO", "ADBE", "NFLX", "CMCSA", "TXN", "AMD", "AMAT", "INTC", "QCOM","HON", "INTU", "SBUX", "BKNG", "MDLZ", "PYPL", "ADI", "PDD", "ADSK", "REGN", "ISRG", "LRCX", "VRTX", "MELI", "GILD", "ABNB", "SNPS", "KLAC", "MRVL", "TEAM","IDXX", "FTNT", "PANW", "WDAY", "ORLY", "CRWD", "ZS", "CDNS", "ANSS", "DXCM", "ASML", "MNST", "ROST", "CPRT", "CTAS", "BIDU", "OKTA", "EXAS", "DOCU", "CHTR","EBAY", "DDOG", "NTES", "VRSK", "LCID", "FAST", "PCAR", "SIRI", "SGEN", "TSCO", "MAR", "PTON", "BIIB", "ATVI", "MTCH", "ROKU", "CTSH", "XEL", "DLTR", "SPLK","PAYC", "CEG", "ALGN", "ZM", "AEP", "UAL", "BKNG", "FOXA", "NLOK", "AMBA", "WYNN", "TTD", "TWLO", "RBLX", "GFS", "NVCR", "SMTC"]
Coin = ["BTC-USD", "ETH-USD", "USDT-USD", "BNB-USD", "USDC-USD", "XRP-USD", "DOGE-USD", "ADA-USD","SOL-USD", "DOT-USD", "MATIC-USD", "LTC-USD", "SHIB-USD", "BCH-USD", "LINK-USD", "XLM-USD","AVAX-USD", "ATOM-USD", "HBAR-USD", "FIL-USD", "TRX-USD", "APE-USD", "ICP-USD", "QNT-USD","NEAR-USD", "LDO-USD", "ALGO-USD", "ARB-USD", "EGLD-USD", "VET-USD", "MANA-USD", "FTM-USD","XTZ-USD", "GRT-USD", "AAVE-USD", "SAND-USD", "STX-USD", "EOS-USD", "CAKE-USD", "KAVA-USD","IMX-USD", "CHZ-USD", "THETA-USD", "ENJ-USD", "WAVES-USD", "RUNE-USD", "1INCH-USD", "BAT-USD","OMG-USD", "ZIL-USD", "CRO-USD", "GALA-USD", "YFI-USD", "COMP-USD", "CRV-USD", "ANKR-USD","SNX-USD", "UNI-USD", "REN-USD", "CELR-USD", "ONT-USD", "RVN-USD", "DASH-USD", "KLAY-USD","FTT-USD", "MINA-USD", "GLMR-USD", "MASK-USD", "DYDX-USD", "MKR-USD", "ZRX-USD", "BAND-USD","BAL-USD", "ROSE-USD", "FLR-USD", "MOVR-USD", "OP-USD", "TWT-USD", "WOO-USD", "NEXO-USD","HOT-USD", "SUSHI-USD", "SRM-USD", "CVC-USD", "LRC-USD", "QTUM-USD", "ICX-USD", "XEC-USD","RLC-USD", "LSK-USD", "GNO-USD", "STEEM-USD", "WAXP-USD", "SXP-USD", "VTHO-USD", "RENBTC-USD","SPELL-USD", "ILV-USD", "AKT-USD", "PENDLE-USD", "NEO-USD", "AERGO-USD"]
bist = ["A1CAP.IS","A1YEN.IS","ACSEL.IS","ADEL.IS","ADESE.IS","ADGYO.IS","AEFES.IS","AFYON.IS","AGESA.IS","AGHOL.IS","AGROT.IS","AGYO.IS","AHGAZ.IS","AHSGY.IS","AKBNK.IS","AKCNS.IS","AKENR.IS","AKFGY.IS","AKFIS.IS","AKFYE.IS","AKGRT.IS","AKMGY.IS","AKSA.IS","AKSEN.IS","AKSGY.IS","AKSUE.IS","AKYHO.IS","ALARK.IS","ALBRK.IS","ALCAR.IS","ALCTL.IS","ALFAS.IS","ALGYO.IS","ALKA.IS","ALKIM.IS","ALKLC.IS","ALTINS1.IS","ALTNY.IS","ALVES.IS","ANELE.IS","ANGEN.IS","ANHYT.IS","ANSGR.IS","ARASE.IS","ARCLK.IS","ARDYZ.IS","ARENA.IS","ARMGD.IS","ARSAN.IS","ARTMS.IS","ARZUM.IS","ASELS.IS","ASGYO.IS","ASTOR.IS","ASUZU.IS","ATAGY.IS","ATAKP.IS","ATATP.IS","ATEKS.IS","ATLAS.IS","ATSYH.IS","AVGYO.IS","AVHOL.IS","AVOD.IS","AVPGY.IS","AVTUR.IS","AYCES.IS","AYDEM.IS","AYEN.IS","AYES.IS","AYGAZ.IS","AZTEK.IS","BAGFS.IS","BAHKM.IS","BAKAB.IS","BALAT.IS","BALSU.IS","BANVT.IS","BARMA.IS","BASCM.IS","BASGZ.IS","BAYRK.IS","BEGYO.IS","BERA.IS","BESLR.IS","BEYAZ.IS","BFREN.IS","BIENY.IS","BIGCH.IS","BIGEN.IS","BIMAS.IS","BINBN.IS","BINHO.IS","BIOEN.IS","BIZIM.IS","BJKAS.IS","BLCYT.IS","BMSCH.IS","BMSTL.IS","BNTAS.IS","BOBET.IS","BORLS.IS","BORSK.IS","BOSSA.IS","BRISA.IS","BRKO.IS","BRKSN.IS","BRKVY.IS","BRLSM.IS","BRMEN.IS","BRSAN.IS","BRYAT.IS","BSOKE.IS","BTCIM.IS","BUCIM.IS","BULGS.IS","BURCE.IS","BURVA.IS","BVSAN.IS","BYDNR.IS","CANTE.IS","CASA.IS","CATES.IS","CCOLA.IS","CELHA.IS","CEMAS.IS","CEMTS.IS","CEMZY.IS","CEOEM.IS","CGCAM.IS","CIMSA.IS","CLEBI.IS","CMBTN.IS","CMENT.IS","CONSE.IS","COSMO.IS","CRDFA.IS","CRFSA.IS","CUSAN.IS","CVKMD.IS","CWENE.IS","DAGHL.IS","DAGI.IS","DAPGM.IS","DARDL.IS","DCTTR.IS","DENGE.IS","DERHL.IS","DERIM.IS","DESA.IS","DESPC.IS","DEVA.IS","DGATE.IS","DGGYO.IS","DGNMO.IS","DIRIT.IS","DITAS.IS","DMRGD.IS","DMSAS.IS","DNISI.IS","DOAS.IS","DOBUR.IS","DOCO.IS","DOFER.IS","DOGUB.IS","DOHOL.IS","DOKTA.IS","DSTKF.IS","DURDO.IS","DURKN.IS","DYOBY.IS","DZGYO.IS","EBEBK.IS","ECILC.IS","ECZYT.IS","EDATA.IS","EDIP.IS","EFORC.IS","EGEEN.IS","EGEGY.IS","EGEPO.IS","EGGUB.IS","EGPRO.IS","EGSER.IS","EKGYO.IS","EKIZ.IS","EKOS.IS","EKSUN.IS","ELITE.IS","EMKEL.IS","EMNIS.IS","ENDAE.IS","ENERY.IS","ENJSA.IS","ENKAI.IS","ENSRI.IS","ENTRA.IS","EPLAS.IS","ERBOS.IS","ERCB.IS","EREGL.IS","ERSU.IS","ESCAR.IS","ESCOM.IS","ESEN.IS","ETILR.IS","ETYAT.IS","EUHOL.IS","EUKYO.IS","EUPWR.IS","EUREN.IS","EUYO.IS","EYGYO.IS","FADE.IS","FENER.IS","FLAP.IS","FMIZP.IS","FONET.IS","FORMT.IS","FORTE.IS","FRIGO.IS","FROTO.IS","FZLGY.IS","GARAN.IS","GARFA.IS","GEDIK.IS","GEDZA.IS","GENIL.IS","GENTS.IS","GEREL.IS","GESAN.IS","GIPTA.IS","GLBMD.IS","GLCVY.IS","GLRMK.IS","GLRYH.IS","GLYHO.IS","GMTAS.IS","GOKNR.IS","GOLTS.IS","GOODY.IS","GOZDE.IS","GRNYO.IS","GRSEL.IS","GRTHO.IS","GSDDE.IS","GSDHO.IS","GSRAY.IS","GUBRF.IS","GUNDG.IS","GWIND.IS","GZNMI.IS","HALKB.IS","HATEK.IS","HATSN.IS","HDFGS.IS","HEDEF.IS","HEKTS.IS","HKTM.IS","HLGYO.IS","HOROZ.IS","HRKET.IS","HTTBT.IS","HUBVC.IS","HUNER.IS","HURGZ.IS","ICBCT.IS","ICUGS.IS","IDGYO.IS","IEYHO.IS","IHAAS.IS","IHEVA.IS","IHGZT.IS","IHLAS.IS","IHLGM.IS","IHYAY.IS","IMASM.IS","INDES.IS","INFO.IS","INGRM.IS","INTEK.IS","INTEM.IS","INVEO.IS","INVES.IS","IPEKE.IS","ISATR.IS","ISBIR.IS","ISBTR.IS","ISCTR.IS","ISDMR.IS","ISFIN.IS","ISGSY.IS","ISGYO.IS","ISKPL.IS","ISKUR.IS","ISMEN.IS","ISSEN.IS","ISYAT.IS","IZENR.IS","IZFAS.IS","IZINV.IS","IZMDC.IS","JANTS.IS","KAPLM.IS","KAREL.IS","KARSN.IS","KARTN.IS","KATMR.IS","KAYSE.IS","KBORU.IS","KCAER.IS","KCHOL.IS","KENT.IS","KERVN.IS","KFEIN.IS","KGYO.IS","KIMMR.IS","KLGYO.IS","KLKIM.IS","KLMSN.IS","KLNMA.IS","KLRHO.IS","KLSER.IS","KLSYN.IS","KLYPV.IS","KMPUR.IS","KNFRT.IS","KOCMT.IS","KONKA.IS","KONTR.IS","KONYA.IS","KOPOL.IS","KORDS.IS","KOTON.IS","KOZAA.IS","KOZAL.IS","KRDMA.IS","KRDMB.IS","KRDMD.IS","KRGYO.IS","KRONT.IS","KRPLS.IS","KRSTL.IS","KRTEK.IS","KRVGD.IS","KSTUR.IS","KTLEV.IS","KTSKR.IS","KUTPO.IS","KUVVA.IS","KUYAS.IS","KZBGY.IS","KZGYO.IS","LIDER.IS","LIDFA.IS","LILAK.IS","LINK.IS","LKMNH.IS","LMKDC.IS","LOGO.IS","LRSHO.IS","LUKSK.IS","LYDHO.IS","LYDYE.IS","MAALT.IS","MACKO.IS","MAGEN.IS","MAKIM.IS","MAKTK.IS","MANAS.IS","MARBL.IS","MARKA.IS","MARTI.IS","MAVI.IS","MEDTR.IS","MEGAP.IS","MEGMT.IS","MEKAG.IS","MEPET.IS","MERCN.IS","MERIT.IS","MERKO.IS","METRO.IS","METUR.IS","MGROS.IS","MHRGY.IS","MIATK.IS","MMCAS.IS","MNDRS.IS","MNDTR.IS","MOBTL.IS","MOGAN.IS","MOPAS.IS","MPARK.IS","MRGYO.IS","MRSHL.IS","MSGYO.IS","MTRKS.IS","MTRYO.IS","MZHLD.IS","NATEN.IS","NETAS.IS","NIBAS.IS","NTGAZ.IS","NTHOL.IS","NUGYO.IS","NUHCM.IS","OBAMS.IS","OBASE.IS","ODAS.IS","ODINE.IS","OFSYM.IS","ONCSM.IS","ONRYT.IS","ORCAY.IS","ORGE.IS","ORMA.IS","OSMEN.IS","OSTIM.IS","OTKAR.IS","OTTO.IS","OYAKC.IS","OYAYO.IS","OYLUM.IS","OYYAT.IS","OZATD.IS","OZGYO.IS","OZKGY.IS","OZRDN.IS","OZSUB.IS","OZYSR.IS","PAGYO.IS","PAMEL.IS","PAPIL.IS","PARSN.IS","PASEU.IS","PATEK.IS","PCILT.IS","PEHOL.IS","PEKGY.IS","PENGD.IS","PENTA.IS","PETKM.IS","PETUN.IS","PGSUS.IS","PINSU.IS","PKART.IS","PKENT.IS","PLTUR.IS","PNLSN.IS","PNSUT.IS","POLHO.IS","POLTK.IS","PRDGS.IS","PRKAB.IS","PRKME.IS","PRZMA.IS","PSDTC.IS","PSGYO.IS","QNBFK.IS","QNBTR.IS","QUAGR.IS","RALYH.IS","RAYSG.IS","REEDR.IS","RGYAS.IS","RNPOL.IS","RODRG.IS","ROYAL.IS","RTALB.IS","RUBNS.IS","RUZYE.IS","RYGYO.IS","RYSAS.IS","SAFKR.IS","SAHOL.IS","SAMAT.IS","SANEL.IS","SANFM.IS","SANKO.IS","SARKY.IS","SASA.IS","SAYAS.IS","SDTTR.IS","SEGMN.IS","SEGYO.IS","SEKFK.IS","SEKUR.IS","SELEC.IS","SELGD.IS","SELVA.IS","SERNT.IS","SEYKM.IS","SILVR.IS","SISE.IS","SKBNK.IS","SKTAS.IS","SKYLP.IS","SKYMD.IS","SMART.IS","SMRTG.IS","SMRVA.IS","SNGYO.IS","SNICA.IS","SNKRN.IS","SNPAM.IS","SODSN.IS","SOKE.IS","SOKM.IS","SONME.IS","SRVGY.IS","SUMAS.IS","SUNTK.IS","SURGY.IS","SUWEN.IS","TABGD.IS","TARKM.IS","TATEN.IS","TATGD.IS","TAVHL.IS","TBORG.IS","TCELL.IS","TCKRC.IS","TDGYO.IS","TEKTU.IS","TERA.IS","TEZOL.IS","TGSAS.IS","THYAO.IS","TKFEN.IS","TKNSA.IS","TLMAN.IS","TMPOL.IS","TMSN.IS","TNZTP.IS","TOASO.IS","TRCAS.IS","TRGYO.IS","TRILC.IS","TSGYO.IS","TSKB.IS","TSPOR.IS","TTKOM.IS","TTRAK.IS","TUCLK.IS","TUKAS.IS","TUPRS.IS","TUREX.IS","TURGG.IS","TURSG.IS","UFUK.IS","ULAS.IS","ULKER.IS","ULUFA.IS","ULUSE.IS","ULUUN.IS","UMPAS.IS","UNLU.IS","USAK.IS","VAKBN.IS","VAKFN.IS","VAKKO.IS","VANGD.IS","VBTYZ.IS","VERTU.IS","VERUS.IS","VESBE.IS","VESTL.IS","VKFYO.IS","VKGYO.IS","VKING.IS","VRGYO.IS","VSNMD.IS","YAPRK.IS","YATAS.IS","YAYLA.IS","YBTAS.IS","YEOTK.IS","YESIL.IS","YGGYO.IS","YGYO.IS","YIGIT.IS","YKBNK.IS","YKSLN.IS","YONGA.IS","YUNSA.IS","YYAPI.IS","YYLGD.IS","ZEDUR.IS","ZOREN.IS","ZRGYO.IS",'XU100.IS','XU030.IS']
bist100 = ['AEFES.IS','AGHOL.IS','AHGAZ.IS','AKBNK.IS','AKCNS.IS','AKFGY.IS','AKFYE.IS','AKSA.IS','AKSEN.IS','ALARK.IS','ALBRK.IS','ALFAS.IS','ARCLK.IS','ASELS.IS','ASTOR.IS','BERA.IS','BIENY.IS','BIMAS.IS','BRSAN.IS','BRYAT.IS','BUCIM.IS','CANTE.IS','CCOLA.IS','CIMSA.IS','CWENE.IS','DOAS.IS','DOHOL.IS','ECILC.IS','ECZYT.IS','EGEEN.IS','ENJSA.IS','ENKAI.IS','EREGL.IS','EUPWR.IS','EUREN.IS','FROTO.IS','GARAN.IS','GENIL.IS','GESAN.IS','GLYHO.IS','GUBRF.IS','HALKB.IS','HEKTS.IS','IMASM.IS','IPEKE.IS','ISCTR.IS','ISDMR.IS','ISMEN.IS','IZMDC.IS','KARSN.IS','KAYSE.IS','KCAER.IS','KCHOL.IS','KMPUR.IS','KONTR.IS','KONYA.IS','KORDS.IS','KOZAA.IS','KOZAL.IS','KRDMD.IS','KZBGY.IS','MAVI.IS','MGROS.IS','MIATK.IS','ODAS.IS','OTKAR.IS','OYAKC.IS','PENTA.IS','PETKM.IS','PGSUS.IS','QUAGR.IS','SAHOL.IS','SASA.IS','SISE.IS','SKBNK.IS','SMRTG.IS','SOKM.IS','TAVHL.IS','TCELL.IS','THYAO.IS','TKFEN.IS','TOASO.IS','TSKB.IS','TTKOM.IS','TTRAK.IS','TUKAS.IS','TUPRS.IS','ULKER.IS','VAKBN.IS','VESBE.IS','YEOTK.IS','YKBNK.IS','YYLGD.IS','ZOREN.IS']
global_Markets = ["^DJI","^GSPC","^IXIC","^RUT","^VIX","^GSPTSE","^BVSP","^MXX","URTH","^GDAXI","^FTSE","^FCHI","^STOXX50E","^AEX","^IBEX","FTSEMIB.MI","^SSMI","^PSI20","BEL20.BR","^ATX","^OMXS30","^OMXC25","IMOEX.ME","RTSI.ME","^WIG20","BUX.BD","XU100.IS","TA35.TA","TASI.SR","^N225","^AXJO","^NZ50","000001.SS","399001.SZ","XIN9.DE","^DJSH","^HSI","^TWII","^SET.BK","^KS11","^JKSE","^NSEI","^BSESN","^PSI","KSE100.KA","^VN30" ]
US_stocks = ["NVDA","WBD","TSLA","NU","F","INTC","HBAN","BAC","AAPL","AMD","CVX","PLTR","AMZN","PFE","IVZ","VALE","SLB","GOOGL","BBD","KEY","XOM","SMCI","ITUB","PBR","SNAP","T","ABEV","BABA","CSX","PCG","BCS","SCHW","RF","CNC","WFC","STLA","MSFT","GOOG","VZ","NOK","AMCR","ABT","MU","MSTR","KMI","KHC","CCL","MRVL","C","TSM","CSCO","USB","AVGO","UNH","HAL","KO","CMCSA","WMT","UBER","HPE","KGC","PEP","TFC","FCX","NEM","ET","META","KVUE","JPM","TEVA","BKR","MRK","OXY","MMM","RKT","PINS","TTD","IPG","DELL","XYZ","BMY","CVE","NFLX","PDD","MDLZ","CNH","VTRS","JNJ","TME","INFY","CAG","ORCL","CMG","DIS","CFG","HLN","AES","CPRT","DOW","PYPL","DAL","NCLH","NKE","GE","CVS","BSX","RBLX","LYG","ELV","LUV","LRCX","NVO","NEE","COP","WMB","MRNA","CTRA","UAL","FAST","KDP","FITB","QCOM","TOST","PG","CPNG","B","PPL","OWL","HPQ","PBR-A","STM","NDAQ","DVN","FNF","PARA","EBAY","GILD","ENPH","ACGL","GM","VST","MDT","RDDT","CHWY","CRM","APH","BP","ALB","VICI","GSK","NSC","EQT","BTI","ANET","BA","RTX","EOG","UNP","VRT","CNP","ON","MO","EXC","BK","CP","IBN","MS","AXP","LNG","D","MNST","XPEV","APA","KR","ASX","ABBV","TGT","SHEL","MCHP","CCI","WBA","PPG","SBUX","HST","DHI","WY","CARR","CL","CNQ","V","CTSH","ARM","SAN","APP","WIT","TROW","EW","OMC","AMAT","ZTS","PM","CZR","CCJ","AFL","UPS","OKE","TXN","MOS","PLD","IBM","DOC","AEP","IOT","SE","TEL","GIS","HUM","TSCO","WDC","IR","DHR","NET","ACN","SO","BEKE","O","BX","MGM","BRK-B","ORLY","FI","BEN","RBRK","NI","ES","EA","BF-B","KMB","CRH","TMUS","BAX","WRB","GEN","EPD","LVS","PCAR","CTVA","SNPS","TAK","FTNT","SRE","HON","VG","DDOG","MOH","DLTR","BBY","CEG","MMC","MCD","BDX","KIM","TJX","UMC","DD","XEL","VLO","DECK","NRG","DASH","TPR","SNOW","GEHC","HD","LLY","CPB","TWLO","STX","BHP","PSX","EQNR","SYF","JCI","SU","TTWO","HES","ACM","HRL","KKR","COF","NWG","SONY","PEG","EIX","AZN","ADM","ABNB","SW","PANW","CB","MUFG","AIG","PGR","IP","ONON","ETN","HDB","APO","STT","CRWD","CNI","RIO","MFG","KMX","TU","CVNA","ADI","AMH","FTV","FE","DG","NWSA","ROST","MTCH","LNT","TMO","ENB","USFD","MPC","DXCM","FSLR","WDAY","MA","LW","DOV","ASML","NTR","AS","ING","LULU","PNC","NVS","CTAS","CAT","TER","ETR","GLW","NXPI","PAYX","AOS","GFI","ICE","APTV","TECK","DUK","INVH","ADBE","ADSK","VTR","LOW","ARES","HSY","FANG","FIS","SMFG","AU","HLT","SYY","IQV","GPN","CF","EL","SJM","LIN","HWM","EXE","TRP","LYB","EC","LEN","OTIS","SHW","CME","FOXA","MFC","SPOT","VIK","BALL","K","CBOE","COST","APD","BCE","CI","MET","WYNN","GEV","WEC","CSGP","CAH","WM","CHD","EVRG","BRO","SWK","AMGN","YUMC","MCO","PNR","BN","PHM","AWK","GS","EMR","FLUT","STZ","ISRG","TAP","EBR","UDR","AEM","COO","VLTO","THC","LMT","HAS","MDB","ZS","TSN","ED","BLDR","EXPD","TECH","EQR","SWKS","FDX","VEEV","NTAP","ALC","DT","DB","STE","SYK","DTE","TRV","LKQ","CLX","GFS","MAS","ADP","JBHT","GD","TD","EQH","ALL","PSTG","HIG","QSR","YUM","TRMB","VIV","HSBC","CMS","HOLX","CRBG","TEAM","BUD","RCI","WELL","DGX","INCY","BAM","ODFL","MAR","CUK","FERG","IFF","VRSK","BIIB","A","BG","INTU","TRU","NUE","WST","ARE","LYV","RCL","AKAM","GPC","TXT","LHX","TRGP","ECL","UBS","MKC","UL","ROL","DLR","CDNS","AEE","NTRS","BXP","MPLX","YPF","RSG","SPGI","IT","PRU","ZBH","REGN","TT","DAY","JBL","GDDY","AMT","CHRW","BBVA","MT","TS","MTB","CCEP","BJ","AMX","HSIC","BSBR","DPZ","NOW","EXPE","RJF","WPM","CHTR","AER","BAH","WCN","WSM","AON","SUI","DE","PWR","DRI","COR","WES","TTE","RBA","HCA","ITW","SAP","PNW","AME","PSA","RVTY","CBRE","BLK","REG","VRTX","XYL","TKO","SPG","L","BNS","ALLE","STLD","SCCO","DEO","CMI","PKG","EMN","RMD","PTC","NOC","PBA","TDY","PFG","IRM","GNRC","CDW","PHG","RELX","WAB","GRMN","VMC","BURL","FOX","NWS","EFX","EXR","RYAN","ATO","GWW","CM","MSI","MAA","WAT","RPM","DVA","WTW","KEYS","CINF","SBS","AJG","POOL","KLAC","ROK","GFL","HUBS","NGG","CPT","IEX","ROP","UHS","MHK","EQIX","SNA","PUK","FRT","HMC","FFIV","GL","MSCI","SOLV","J","LH","GGG","FTS","SLF","HUBB","BEP","HII","AVY","WDS","KEP","GWRE","RL","TEF","BIP","RS","MCK","BR","CRL","PH","PAYC","RY","AVB","ALGN","LDOS","NDSN","EPAM","FNV","TLK","BMO","MPWR","CPAY","JKHY","NMR","ZBRA","FDS","ULTA","EME","MLM","AMP","FMX","AXON","ULS","SBAC","URI","RACE","MKTX","AIZ","VRSN","BCH","PODD","TM","HEI","IDXX","MELI","CSL","ESS","BAP","GIB","EG","KB","TYL","WSO","FIX","TDG","LII","ERIE","E","FMS","KOF","CW","IHG","FICO","CQP","HEI-A","CHT","BF-A","BKNG","TPL","SHG","IX","AZO","UI","MTD","MKL","LEN-B","MKC-V","NVR","BBDO","BRK-A","WSO-B"]
portfolio = ["MGROS.IS","KCHOL.IS","THYAO.IS","KRDMD.IS","CCOLA.IS","BRSAN.IS","ZOREN.IS","TTRAK.IS","AEFES.IS","FROTO.IS","ALCAR.IS","ISCTR.IS"] 

def classic_analysis(Stock_List,timespan,period):
    stock_dict = {}
    stock_data = []
    stock_number = 0
    for stocks in Stock_List:
        #time.sleep(1)
        try:
            ticker = yf.Ticker(stocks)
            stock_info = ticker.info
            data = {key: stock_info.get(key, None) for key in ["symbol", "priceToBook", "currentPrice", "targetHighPrice", "targetLowPrice", "targetMeanPrice", "targetMedianPrice",
                                                                "bookValue", "open", "dayLow", "dayHigh", "recommendationKey", 'fiftyTwoWeekLow', 'fiftyTwoWeekHigh']}
            historical_data = ticker.history(period="2y",interval=timespan)  # Get historical data for the stock
            #historical_data = yf.download(stocks, period=period, interval=timespan)
            stock_dict[stocks] = historical_data
            if historical_data.empty:
                print(f"No historical data for {stocks}, skipping...")
                continue  # Skip this ticker if no historical data is found
            stock_number = 1 + stock_number
            print(f"\r{stock_number}/{len(Stock_List)} Downloaded {stocks} data", end='', flush=True)

            historical_data['RSI'] = ta.rsi(historical_data['Close'], length=14)  # Calculate RSI (Relative Strength Index)
            adx_data = ta.adx(historical_data['High'], historical_data['Low'], historical_data['Close'], length=14)  # Calculate ADX (Average Directional Index)
            historical_data['ADX'] = adx_data['ADX_14']
            macd = ta.macd(historical_data['Close'], fast=12, slow=26, signal=9)
            historical_data = pd.concat([historical_data, macd], axis=1)
            # Indicators
            
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
            historical_data['SMA_14'] = ta.sma(historical_data['Close'], length=14)
            historical_data['SMA_20'] = ta.sma(historical_data['Close'], length=20)
            historical_data['SMA_50'] = ta.sma(historical_data['Close'], length=50)
            historical_data['SMA_100'] = ta.sma(historical_data['Close'], length=100)
            historical_data['SMA_200'] = ta.sma(historical_data['Close'], length=200)
            historical_data['EMA_200'] = ta.ema(historical_data['Close'], length=200)
            ichimoku = ta.ichimoku(historical_data['High'], historical_data['Low'], historical_data['Close'],tenkan=9, kijun=26, senkou=52, offset=26,include_chikou=True)
            # Handle Ichimoku data structure - it returns a tuple of DataFrames
            if isinstance(ichimoku, tuple) and len(ichimoku) >= 2:
                ichi_df1, ichi_df2 = ichimoku[0], ichimoku[1]
                historical_data['Tenkan'] = ichi_df1['ITS_9'] if 'ITS_9' in ichi_df1.columns else None
                historical_data['Kijun'] = ichi_df1['IKS_26'] if 'IKS_26' in ichi_df1.columns else None
                historical_data['Senkou_A'] = ichi_df1['ISA_9'] if 'ISA_9' in ichi_df1.columns else None
                historical_data['Senkou_B'] = ichi_df1['ISB_26'] if 'ISB_26' in ichi_df1.columns else None
                historical_data['Chikou'] = ichi_df2['ICS_26'] if 'ICS_26' in ichi_df2.columns else None
            else:
                # Fallback if structure is different
                historical_data['Tenkan'] = None
                historical_data['Kijun'] = None
                historical_data['Senkou_A'] = None
                historical_data['Senkou_B'] = None
                historical_data['Chikou'] = None
            
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
            historical_data['BB_Lower'] =  bollinger.iloc[:, 0]  # Lower Band
            historical_data['BB_Middle'] = bollinger.iloc[:, 1]  # Middle Band
            historical_data['BB_Upper'] =  bollinger.iloc[:, 2]  # Upper Band
            historical_data['BB_BWidth'] = bollinger.iloc[:, 3]  # Bandwidth
            historical_data['BB_%B'] =     bollinger.iloc[:, 4]  # %B

            data.update({"RSI": historical_data['RSI'].iloc[-1], "ADX": historical_data['ADX'].iloc[-1],"CCI": historical_data['CCI'].iloc[-1], "ROC": historical_data['ROC'].iloc[-1], "ATR": historical_data['ATR'].iloc[-1], "OBV": historical_data['OBV'].iloc[-1],
                        "CMF": historical_data['CMF'].iloc[-1], "AD": historical_data['AD'].iloc[-1], "MFI": historical_data['MFI'].iloc[-1],
                        "MACD": historical_data['MACD_12_26_9'].iloc[-1],"MACD_signal": historical_data['MACDs_12_26_9'].iloc[-1],"MACD_Hist": historical_data['MACDh_12_26_9'].iloc[-1],"MACDAS": historical_data['MACDAS'].iloc[-1],"MACDAS_Signal": historical_data['MACDAS_Signal'].iloc[-1],
                        "BB_Middle": historical_data['BB_Middle'].iloc[-1],"BB_Upper": historical_data['BB_Upper'].iloc[-1],"BB_Lower": historical_data['BB_Lower'].iloc[-1],'BB_%B': historical_data['BB_%B'].iloc[-1],'BB_BWidth': historical_data['BB_BWidth'].iloc[-1],
                        "FWMA": historical_data["FWMA"].iloc[-1],"VWAP": historical_data["VWAP"].iloc[-1],
                        "kama" : historical_data["kama"].iloc[-1],
                        #"PSAR": historical_data['PSAR'].iloc[-1] if pd.notna(historical_data['PSAR'].iloc[-1]) else None,
                        #"psar" : historical_data["psar"].iloc[-1],
                        "EMA_200": historical_data['EMA_200'].iloc[-1] if pd.notna(historical_data['EMA_200'].iloc[-1]) else None,
                        "Supertrend": historical_data['Supertrend'].iloc[-1],
                        "Supertrend_direction": historical_data['Supertrend_direction'].iloc[-1],
                        "Stoch_K": historical_data['Stoch_K'].iloc[-1],
                        "Stoch_D": historical_data['Stoch_D'].iloc[-1],
                        "StochRSI_K": historical_data['StochRSI_K'].iloc[-1],
                        "StochRSI_D": historical_data['StochRSI_D'].iloc[-1],
                        "Tenkan": historical_data['Tenkan'].iloc[-1] if historical_data['Tenkan'].iloc[-1] is not None else None,
                        "Kijun": historical_data['Kijun'].iloc[-1] if historical_data['Kijun'].iloc[-1] is not None else None,
                        "Senkou_A": historical_data['Senkou_A'].iloc[-1] if historical_data['Senkou_A'].iloc[-1] is not None else None,
                        "Senkou_B": historical_data['Senkou_B'].iloc[-1] if historical_data['Senkou_B'].iloc[-1] is not None else None,
                        "Chikou": historical_data['Chikou'].iloc[-1] if historical_data['Chikou'].iloc[-1] is not None else None,
                        "SMA_14": historical_data['SMA_14'].iloc[-1],
                        "SMA_20": historical_data['SMA_20'].iloc[-1],
                        "SMA_50": historical_data['SMA_50'].iloc[-1],
                        "SMA_100": historical_data['SMA_100'].iloc[-1],
                        "SMA_200": historical_data['SMA_200'].iloc[-1],
                        })
            stock_data.append(data)

        except Exception as e:
            print(f"Error fetching data for {stocks}: {e}")

    # Create a DataFrame from the stock data
    df = pd.DataFrame(stock_data)
    df["time"] = datetime.now()
    df["YF%"] = ((df["currentPrice"] - df["fiftyTwoWeekLow"])/(df["fiftyTwoWeekHigh"]-df["fiftyTwoWeekLow"]))*100 #Check the differences
    df["MACDAS-dif"] = df["MACDAS"] - df["MACDAS_Signal"] 
    df["change"] = ((df["currentPrice"] / df["open"]) - 1) * 100
    df["BB_Pot"] = ((df['BB_Upper'] / df["currentPrice"]) - 1) * 100
    df["BB_Opt"] = ((df['BB_Lower'] / df["currentPrice"]) - 1) * 100
    df["TrendWay"] = np.select([(df["ADX"] > 20) & (df["ROC"] > 0), (df["ADX"] > 20) & (df["ROC"] <= 0), (df["ADX"] <= 20)], ["upper", "lower", "no-trend"], default="unknown")
    
    # Add Ichimoku Cloud Analysis (only if data is available)
    df["Cloud_Position"] = np.select([
        (df["currentPrice"] > df["Senkou_A"]) & (df["currentPrice"] > df["Senkou_B"]) & df["Senkou_A"].notna() & df["Senkou_B"].notna(),
        (df["currentPrice"] < df["Senkou_A"]) & (df["currentPrice"] < df["Senkou_B"]) & df["Senkou_A"].notna() & df["Senkou_B"].notna()
    ], ["Above_Cloud", "Below_Cloud"], default="No_Data")
    
    df["TK_Cross"] = np.select([
        (df["Tenkan"] > df["Kijun"]) & df["Tenkan"].notna() & df["Kijun"].notna(),
        (df["Tenkan"] < df["Kijun"]) & df["Tenkan"].notna() & df["Kijun"].notna()
    ], ["Bullish", "Bearish"], default="No_Data")
    # removed indicators = ("OBV","AD","Stoch_K","Stoch_D","Chikou",)
    #df1 = df[["symbol","time", "StochRSI_K","StochRSI_D","MACDAS-dif","MACDAS","MACDAS_Signal", 'BB_BWidth', 'BB_%B',"YF%","MFI", "RSI", "ADX", "CCI", "ROC","CMF", "ATR","FWMA","VWAP","Supertrend","Supertrend_direction","kama", "Tenkan","Kijun","Senkou_A","Senkou_B","Cloud_Position","TK_Cross","currentPrice","change","EMA_200"]]
    df2 = df.rename(columns={"currentPrice": "CPrice","Supertrend_direction":"st_way"})

    #pd.set_option('display.float_format', '{:.2f}'.format)
    print("\nDownload process is done!")
    now = datetime.now().strftime("%d_%m_%y")
    #formatted_time = now.strftime("%d_%m_%y")
    df2.to_csv(f"CSVs/Results last.csv")
    if Stock_List == bist:
        df2.to_csv(f"CSVs/Results/bist_{now}.csv")
    elif Stock_List == US_stocks:
        df2.to_csv(f"CSVs/Results/US_stocks_{now}.csv")
    elif Stock_List == portfolio:
        df2.to_csv(f"CSVs/Results/portfolio_{now}.csv")    
    else:
        print("Saving Process Failed!")
    print("Stock Market Data Processing is Done!")
#classic_analysis(portfolio)