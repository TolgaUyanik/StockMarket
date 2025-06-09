import yfinance as yf

bist = ["AEFES.IS", "AGHOL.IS", "AHGAZ.IS", "AKBNK.IS", "AKCNS.IS", "AKFGY.IS", "AKFYE.IS", "AKSA.IS",  "AKSEN.IS", "ALARK.IS", "ALBRK.IS", "ALFAS.IS", "ARCLK.IS", "ASELS.IS", "ASTOR.IS", "BERA.IS", "BIENY.IS",
        "BIMAS.IS", "BRSAN.IS", "BRYAT.IS", "BUCIM.IS", "CANTE.IS", "CCOLA.IS", "CIMSA.IS", "CWENE.IS", "DOAS.IS",  "DOHOL.IS", "ECILC.IS", "ECZYT.IS", "EGEEN.IS", "EKGYO.IS", "ENJSA.IS", "ENKAI.IS", "EREGL.IS",
        "EUPWR.IS", "EUREN.IS", "FROTO.IS", "GARAN.IS", "GENIL.IS", "GESAN.IS", "GLYHO.IS", "GUBRF.IS", "GWIND.IS", "HALKB.IS", "HEKTS.IS", "IMASM.IS", "IPEKE.IS", "ISCTR.IS", "ISDMR.IS", "ISGYO.IS", "ISMEN.IS",
        "IZMDC.IS", "KARSN.IS", "KAYSE.IS", "KCAER.IS", "KCHOL.IS", "KMPUR.IS", "KONTR.IS", "KONYA.IS", "KORDS.IS", "KOZAA.IS", "KOZAL.IS", "KRDMD.IS", "KZBGY.IS", "MAVI.IS",  "MGROS.IS", "MIATK.IS", "ODAS.IS",
        "OTKAR.IS", "OYAKC.IS", "PENTA.IS", "PETKM.IS", "PGSUS.IS", "PSGYO.IS", "QUAGR.IS", "SAHOL.IS", "SASA.IS",  "SISE.IS",  "SKBNK.IS", "SMRTG.IS", "SNGYO.IS", "SOKM.IS",  "TAVHL.IS", "TCELL.IS", "THYAO.IS",
        "TKFEN.IS", "TOASO.IS", "TSKB.IS",  "TTKOM.IS", "TTRAK.IS", "TUKAS.IS", "TUPRS.IS", "ULKER.IS", "VAKBN.IS", "VESBE.IS", "VESTL.IS", "YEOTK.IS", "YKBNK.IS", "YYLGD.IS", "ZOREN.IS"]


xgida = ["AEFES.IS","ATAKP.IS","AVOD.IS","BANVT.IS","CCOLA.IS","DARDL.IS","DMRGD.IS","EKSUN.IS","ELITE.IS","ERSU.IS","FADE.IS","FRIGO.IS","GOKNR.IS","KAYSE.IS","KERVT.IS","KRVGD.IS",
         "KNFRT.IS","KRSTL.IS","KTSKR.IS","MERKO.IS","ORCAY.IS","OYLUM.IS","PENGD.IS","PETUN.IS","PINSU.IS","PNSUT.IS","SELGD.IS","SELVA.IS","SOKE.IS","TATGD.IS",
         "TETMT.IS","TUKAS.IS","ULUUN.IS","ULKER.IS","VANGD.IS","YYLGD.IS",]
#,"OFSYM.IS"

Xkmya = ["ACSEL.IS","AKSAA.IS","ALKIM.IS","ANGEN.IS","AYGAZ.IS","BAGFS.IS","BAYRK.IS","BRKSN.IS","BRISA.IS","DEVAD.IS","DNISI.IS","DYOBY.IS","EGGUB.IS","EGPRO.IS","EPLAS.IS",
         "EUREN.IS","GEDZA.IS","GOODY.IS","GUBRF.IS","HEKTS.IS","ISKPL.IS","IZFAS.IS","KMPUR.IS","KRPLS.IS","KOPOL.IS","KBORU.IS","MRSHL.IS","MEDTR.IS","MERCN.IS","ONCSM.IS",
         "OZRDN.IS","PETKM.IS","POLTK.IS","RNPOL.IS","RTALB.IS","SANFM.IS","SASAS.IS","SEKUR.IS","SEYKM.IS","TARKM.IS","TMPOL.IS","TRILC.IS","TUPRS.IS"]

Xmadn = ["ALMAD.IS", "CVKMD.IS", "IPEKE.IS", "KOZAL.IS", "KOZAA.IS", "PRKME.IS"]

Xmtal = ["BMSTL.IS","BMSCH.IS","BRSAN.IS","BURCE.IS","BURVA.IS","CELHA.IS","CEMAS.IS","CEMTS.IS","CUSAN.IS","DMSAS.IS","DOFER.IS","DOKTA.IS","ERBOS.IS","ERCBE.IS",
         "EREGL.IS","ISDMR.IS","IZMDC.IS","KRDMA.IS","KRDMB.IS","KRDMD.IS","KCAER.IS","MEGMT.IS","PNLSN.IS","SARKY.IS","TUCLK.IS","YKSLN.IS",]

Xmesy = ["ALCAR.IS","ASUZU.IS","ARCLK.IS","ASTOR.IS","BNTAS.IS","BFREN.IS","BVSAN.IS","DITAS.IS","EGEEN.IS","EKOSE.IS","EMKEL.IS","EUPWR.IS","FMIZP.IS","FROTO.IS","FORMT.IS",
         "GEREL.IS","HATSN.IS","HKTMH.IS","IHEVA.IS","IMASM.IS","JANTS.IS","KARSN.IS","KATMR.IS","KLMSN.IS","MAKIM.IS","MAKTK.IS","MEKAG.IS","OTKAR.IS","PARSN.IS","SAFKR.IS",
         "SNICA.IS","SAYAS.IS","SILVR.IS","TOASO.IS","TMSNT.IS","PRKAB.IS","TTRAK.IS","ULUSE.IS","VESBE.IS","VESTL.IS"]

Xkagt = ["ALKAA.IS","BAKAB.IS","BARMA.IS","DGNMO.IS","DURDO.IS","TEZOL.IS","GENTS.IS","GIPTA.IS","KAPLM.IS","KARTN.IS","KLSYN.IS","KONKA.IS","MNDTR.IS","PRZMA.IS",
         "SAMAT.IS","VKING.IS",]

Xtast = ["AFYON.IS","AKCNS.IS","BTCIM.IS","BSOKE.IS","BIENY.IS","BOBET.IS","BUCIM.IS","CMBTN.IS","CIMSA.IS","DOGUB.IS","EGSER.IS","GOLTS.IS","KLKIM.IS","KLSER.IS","KONYA.IS",
         "KUTPO.IS","NIBAS.IS","NUHCM.IS","OYAKC.IS","QUAGR.IS","MARBL.IS","USAKU.IS",]

Xtest = ["ATEKS.IS","ARSAN.IS","BLCYT.IS","BOSSA.IS","DAGID.IS","DERIM.IS","DESAD.IS","ENSRI.IS","HATEK.IS","ISSEN.IS","KRTEK.IS","KORDS.IS","LUKSK.IS","MEGAP.IS","MNDRS.IS",
         "RODRG.IS","RUBNS.IS","SKTAS.IS","SUNTK.IS","YATAS.IS","YUNSA.IS",]

xuhiz = ["ADESE.IS","AHGAZ.IS","AKENR.IS","AKFYE.IS","AKSEN.IS","AKSUE.IS","ALFAS.IS","AYCES.IS","ANELE.IS","ARZUM.IS","AVTUR.IS","AYDEM.IS","AYENA.IS","BYDNR.IS","BJKAS.IS",
         "BEYAZ.IS","BIMAS.IS","BIOEN.IS","BRLSM.IS","BIZIM.IS","BORLS.IS","BIGCH.IS","CRFSA.IS","CEOEM.IS","CONSE.IS","CWENE.IS","CANTE.IS","CATES.IS","CLEBI.IS","DAPGM.IS",
         "DOCOD.IS","DOBUR.IS","ARASE.IS","DOASD.IS","EBEBK.IS","EDIPE.IS","ENJSA.IS","ENERY.IS","ENKAI.IS","KIMMR.IS","ESCAR.IS","ESENE.IS","ETILR.IS","FENER.IS","FLAPF.IS",
         "GWIND.IS","GSRAY.IS","GENIL.IS","GZNMI.IS","GMTAS.IS","GESAN.IS","GRTRK.IS","GSDDE.IS","GRSEL.IS","HUNER.IS","HURGZ.IS","IDEAS.IS","IHLGM.IS","IHGZT.IS","IHAAS.IS",
         "INTEM.IS","IZENR.IS","KARYE.IS","KONTR.IS","KUYAS.IS","LIDER.IS","LKMNH.IS","MACKO.IS","MAGEN.IS","MAALT.IS","MARTI.IS","MAVIM.IS","MEPET.IS","MERIT.IS","MGROS.IS",
         "MIPAZ.IS","MPARK.IS","EGEPO.IS","NATEN.IS","NTGAZ.IS","ODASO.IS","ORGEO.IS","PAMEL.IS","PASEU.IS","PCILT.IS","PGSUS.IS","PSDTC.IS","PKENT.IS","PLTUR.IS","RYSAS.IS",
         "SANEL.IS","SANKO.IS","SELEC.IS","SMRTG.IS","SONME.IS","SUWEN.IS","SOKMŞ.IS","TABGD.IS","TNZTP.IS","TATEN.IS","TEKTU.IS","TKNSA.IS","TGSAS.IS","TLMAN.IS","TSPOR.IS",
         "TUREX.IS","TCELL.IS","THYAO.IS","TTKOM.IS","TURGG.IS","ULASU.IS","VAKKO.IS","YAYLA.IS","YEOTK.IS","YYAPI.IS","ZEDUR.IS","ZOREN.IS",]
Xelkt = ["AHGAZ.IS","AKENR.IS","AKFYE.IS","AKSEN.IS","AKSUE.IS","ALFAS.IS","AYDEM.IS","AYENA.IS","BIOEN.IS","CONSE.IS","CWENE.IS","CANTE.IS","CATES.IS","ARASE.IS","ENJSA.IS",
         "ENERY.IS","ESENE.IS","GWIND.IS","HUNER.IS","IZENR.IS","KARYE.IS","MAGEN.IS","NATEN.IS","NTGAZ.IS","ODASO.IS","PAMEL.IS","SMRTG.IS","TATEN.IS","ZEDUR.IS","ZOREN.IS",]

Xiltm =["TCELL.IS","TTKOM.IS"]

Xinsa = ["ANELE.IS","BRLSM.IS","DAPGM.IS","EDIPE.IS","ENKAI.IS","GESAN.IS","KUYAS.IS","ORGEO.IS","SANEL.IS","TURGG.IS","YAYLA.IS","YYAPI.IS"]

Xtcrt = ["ARZUM.IS","BIMAS.IS","BIZIM.IS","CRFSA.IS","DOASD.IS","EBEBK.IS","KIMMR.IS","GENIL.IS","GMTAS.IS","GRTRK.IS","INTEM.IS","MAVI.IS","MEPET.IS","MGROS.IS","MIPAZ.IS",
         "PSDTC.IS","SANKO.IS","SELEC.IS","SUWEN.IS","SOKM.IS","TKNSA.IS","TGSAS.IS","VAKKO.IS",]
Xtrzm = ["AYCES.IS","AVTUR.IS","BYDNR.IS","BIGCH.IS","DOCOD.IS","ETILR.IS","MAALT.IS","MARTI.IS","MERIT.IS","PKENT.IS","TABGD.IS","TEKTU.IS","ULASU.IS"]

Xmali = ["ADGYO.IS","AGHOL.IS","AGESA.IS","AKBNK.IS","AKYHO.IS","AKFGY.IS","AKSGY.IS","AKMGY.IS","AKGRT.IS","ALGYO.IS","ALARK.IS","ALBRK.IS","ANSGR.IS","ANHYT.IS","ASGYO.IS",
         "ATAGY.IS","AGYOA.IS","AVGYO.IS","AVHOL.IS","AVPGY.IS","A1CAP.IS","BASGZ.IS","BEGYO.IS","BERAB.IS","BRKVY.IS","BRYAT.IS","COSMO.IS","CRDFA.IS","DAGHL.IS","DENGE.IS",
         "DZGYO.IS","DERHL.IS","DOHOL.IS","DGGYO.IS","ECZYT.IS","ECILC.IS","EKGYO.IS","EUHOL.IS","EYGYO.IS","FZLGY.IS","GARFA.IS","GEDIK.IS","GLCVY.IS","GLBMD.IS","GLYHO.IS",
         "GOZDE.IS","GSDHO.IS","GLRYH.IS","SAHOL.IS","HLGYO.IS","HDFGS.IS","HEDEF.IS","HUBVC.IS","ICBCT.IS","ICUGS.IS","INVEO.IS","INVES.IS","IEYHO.IS","IDGYO.IS","IHLAS.IS",
         "IHYAY.IS","INFO.IS""ISFIN.IS","ISGYO.IS","ISGSY.IS","ISMEN.IS","KTLEV.IS","KZBGY.IS","KLGYO.IS","KLRHO.IS","KCHOL.IS","KGYOK.IS","KRGYO.IS","KZGYO.IS","LIDFA.IS",
         "LRSHO.IS","MARKA.IS","MRGYO.IS","MZHLD.IS","METUR.IS","METRO.IS","MHRGY.IS","MSGYO.IS","NTHOL.IS","NUGYO.IS","OSMEN.IS","OSTIM.IS","OYYAT.IS","OZKGY.IS","OZGYO.IS",
         "PAGYO.IS","PRDGS.IS","PSGYO.IS","PEKGY.IS","PEGYO.IS","POLHO.IS","RALYH.IS","RAYSG.IS","RYGYO.IS","SRVGY.IS","SNGYO.IS","SURGY.IS","SEKFK.IS","SEGYO.IS","SKYMD.IS",
         "SKBNK.IS","TAVHL.IS","TKFEN.IS","TERAT.IS","TRGYO.IS","TDGYO.IS","TSGYO.IS","TRCAS.IS","GARAN.IS","HALKB.IS","ISATR.IS","ISBTR.IS","ISCTR.IS","TSKBT.IS","TURSG.IS",
         "SISET.IS","VAKBN.IS","UFUKU.IS","ULUFA.IS","UNLU.IS""VAKFN.IS","VKGYO.IS","VRGYO.IS","VERUS.IS","VERTU.IS","YKBNK.IS","YGGYO.IS","YGYOY.IS","YESIL.IS","ZRGYO.IS","BINHO.IS"]

Xbank = ["AKBNK.IS","ALBRK.IS","ICBCT.IS","SKBNK.IS","GARAN.IS","HALKB.IS","ISCTR.IS","ISATR.IS","ISBTR.IS","TSKBT.IS","VAKBN.IS","YKBNK.IS"]

Xsgrt = ["AGESA.IS", "AKGRT.IS", "ANSGR.IS", "ANHYT.IS", "RAYSG.IS", "TURSG.IS"]

Xhold = ["AGHOL.IS","AKYHO.IS","ALARK.IS","AVHOL.IS","BERAB.IS","BRYAT.IS","COSMO.IS","DAGHL.IS","DENGE.IS","DERHL.IS","DOHOL.IS","ECZYT.IS","ECILC.IS","EUHOL.IS","GLYHO.IS",
         "GOZDE.IS","GSDHO.IS","GLRYH.IS","SAHOL.IS","HDFGS.IS","HEDEF.IS","HUBVC.IS","ICUGS.IS","INVEO.IS","INVES.IS","IEYHO.IS","IHLAS.IS","IHYAY.IS","ISGSY.IS","KLRHO.IS",
         "KCHOL.IS","LRSHO.IS","MARKA.IS","MZHLD.IS","METUR.IS","METRO.IS","NTHOL.IS","OSTIM.IS","PRDGS.IS","POLHO.IS","RALYH.IS","TAVHL.IS","TKFEN.IS","TRCAS.IS","SISET.IS",
         "UFUKU.IS","UNLU.IS","VERUS.IS","VERTU.IS","YESIL.IS","BINHO.IS"]

Xgyo =  ["ADGYO.IS","AKFGY.IS","AKSGY.IS","AKMGY.IS","ALGYO.IS","ASGYO.IS","ATAGY.IS","AGYOA.IS","AVGYO.IS","AVPGY.IS","BASGZ.IS","BEGYO.IS","DZGYO.IS","DGGYO.IS","EKGYO.IS",
         "EYGYO.IS","FZLGY.IS","HLGYO.IS","IDGYO.IS","ISGYO.IS","KZBGY.IS","KLGYO.IS","KGYOK.IS","KRGYO.IS","KZGYO.IS","MRGYO.IS","MHRGY.IS","MSGYO.IS","NUGYO.IS","OZKGY.IS",
         "OZGYO.IS","PAGYO.IS","PSGYO.IS","PEKGY.IS","PEGYO.IS","RYGYO.IS","SRVGY.IS","SNGYO.IS","SURGY.IS","SEGYO.IS","TRGYO.IS","TDGYO.IS","TSGYO.IS","VKGYO.IS","VRGYO.IS",
         "YGGYO.IS","YGYO.IS","ZRGYO.IS"]

Xutek = ["ALCTL.IS","ARDYZ.IS","ARENA.IS","ASELS.IS","ATATP.IS","AZTEK.IS","DGATE.IS","DESPC.IS","EDATA.IS","ESCOM.IS","FONET.IS","FORTE.IS","HTTBT.IS","INGRM.IS","INDES.IS",
         "KFEIN.IS","KAREL.IS","KRONT.IS","LINKL.IS","LOGOL.IS","MANAS.IS","MTRKS.IS","MIATK.IS","MOBTL.IS","NETAS.IS","OBASE.IS","PAPIL.IS","PENTA.IS","PKART.IS","REEDR.IS",
         "SDTTR.IS","SMART.IS","VBTYZ.IS"]

Xblsm = ["ALCTL.IS","ARDYZ.IS","ARENA.IS","ATATP.IS","AZTEK.IS","DGATE.IS","DESPC.IS","EDATA.IS","ESCOM.IS","FONET.IS","FORTE.IS","HTTBT.IS","INGRM.IS","INDES.IS","KFEIN.IS",
         "KAREL.IS","KRONT.IS","LINKL.IS","LOGOL.IS","MANAS.IS","MTRKS.IS","MIATK.IS","MOBTL.IS","NETAS.IS","OBASE.IS","PAPIL.IS","PENTA.IS","PKART.IS","REEDR.IS","SMART.IS",
         "VBTYZ.IS",]

#bistten sonra bir loop yaratıp hepsini ayrı ayrı çalıştırabiliriz

shorttrade= ["Shorttrade"]
longtrade = ["Longtrade"]
speculation_decetor =["There is a spek"]




for stocks in xgida:
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
    
    
    speculation = ((dayHigh/dayLow)-1)*100
    change= ((currentPrice/previousClose)-1)*100
    
    print(stocks)
    print(bookValue)
    print(pricetoBook)
    #print(fiftytwoweeklow)
    
    #print(previousClose)
    #print(currentPrice)
    print(change)
    if abs(change) > 3:
        shorttrade.append(stocks)
        shorttrade.append(change)
    else:
        pass

    if abs(speculation) > 6:
        speculation_decetor.append(stocks)
        speculation_decetor.append(speculation) 



    if pricetoBook < 2:
        longtrade.append(stocks)
        longtrade.append(pricetoBook)
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