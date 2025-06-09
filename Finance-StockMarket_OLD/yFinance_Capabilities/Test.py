import yfinance as yf

# Replace 'AAPL' with your desired stock symbol
symbol = "XU100.IS"
# Create a Ticker object
ticker = yf.Ticker(symbol)
# Get general information about the stock
stock_info = ticker.info
# Print the information
print(stock_info)
"""
{'name': 'Bitcoin', 'startDate': 1278979200, 'description': 'Bitcoin (BTC) is a cryptocurrency launched in 2010. Users are able to generate BTC through the process of mining. 
 Bitcoin has a current supply of 19,657,468. The last known price of Bitcoin is 68,000.63113187 USD and is up 2.52 over the last 24 hours. It is currently trading on 10927 
 active market(s) with $41,308,633,553.35 traded over the last 24 hours. More information can be found at https://bitcoin.org/.', 'maxAge': 86400, 'priceHint': 2, 
 'previousClose': 68362.83, 'open': 68362.83, 'dayLow': 66679.305, 'dayHigh': 68844.13, 'regularMarketPreviousClose': 68362.83, 'regularMarketOpen': 68362.83, 
 'regularMarketDayLow': 66679.305, 'regularMarketDayHigh': 68844.13, 'volume': 48794267648, 'regularMarketVolume': 48794267648, 'averageVolume': 31592261745, 
 'averageVolume10days': 52245425966, 'averageDailyVolume10Day': 52245425966, 'marketCap': 1319779827712, 'fiftyTwoWeekLow': 24797.168, 'fiftyTwoWeekHigh': 73750.07, 
 'fiftyDayAverage': 55341.09, 'twoHundredDayAverage': 40405.453, 'currency': 'USD', 'fromCurrency': 'BTC', 'toCurrency': 'USD=X', 'lastMarket': 'CoinMarketCap', 
 'coinMarketCapLink': 'https://coinmarketcap.com/currencies/bitcoin', 'volume24Hr': 48794267648, 'volumeAllCurrencies': 48794267648, 'circulatingSupply': 19657906, 
 'exchange': 'CCC', 'quoteType': 'CRYPTOCURRENCY', 'symbol': 'BTC-USD', 'underlyingSymbol': 'BTC-USD', 'shortName': 'Bitcoin USD', 'longName': 'Bitcoin USD', 
 'firstTradeDateEpochUtc': 1410912000, 'timeZoneFullName': 'UTC', 'timeZoneShortName': 'UTC', 'uuid': '74397779-1589-3270-8c45-b7f1a7345b3a', 'messageBoardId': 'finmb_BTC_CCC',
   'trailingPegRatio': None}
"""
{'maxAge': 86400, 'priceHint': 2, 'previousClose': 11127.56, 'open': 11151.47, 'dayLow': 11060.67, 'dayHigh': 11195.98, 'regularMarketPreviousClose': 11127.56,
  'regularMarketOpen': 11151.47, 'regularMarketDayLow': 11060.67, 'regularMarketDayHigh': 11195.98, 'volume': 0, 'regularMarketVolume': 0, 'averageVolume': 1776808,
    'averageVolume10days': 1577510, 'averageDailyVolume10Day': 1577510, 'bid': 0.0, 'ask': 0.0, 'bidSize': 0, 'askSize': 0, 'fiftyTwoWeekLow': 4848.6, 'fiftyTwoWeekHigh': 11314.3,
      'fiftyDayAverage': 10047.118, 'twoHundredDayAverage': 8863.649, 'currency': 'TRY', 'exchange': 'IST', 'quoteType': 'INDEX', 'symbol': 'XU030.IS', 'underlyingSymbol': 'XU030.IS',
        'shortName': 'BIST 30', 'longName': 'BIST 30', 'firstTradeDateEpochUtc': 852190200, 'timeZoneFullName': 'Europe/Istanbul', 'timeZoneShortName': 'TRT',
          'uuid': '8b4ab60c-ef84-31bf-a07e-aade85774c92', 'messageBoardId': 'finmb_INDEXXU030.IS', 'gmtOffSetMilliseconds': 10800000, 'trailingPegRatio': None}
{'maxAge': 86400, 'priceHint': 2, 'previousClose': 10247.75, 'open': 10274.38, 'dayLow': 10187.83, 'dayHigh': 10304.29, 'regularMarketPreviousClose': 10247.75,
  'regularMarketOpen': 10274.38, 'regularMarketDayLow': 10187.83, 'regularMarketDayHigh': 10304.29, 'volume': 0, 'regularMarketVolume': 0, 'averageVolume': 3070016396,
    'averageVolume10days': 3060148670, 'averageDailyVolume10Day': 3060148670, 'bid': 0.0, 'ask': 0.0, 'bidSize': 0, 'askSize': 0, 'fiftyTwoWeekLow': 4404.1, 'fiftyTwoWeekHigh': 10383.3,
      'fiftyDayAverage': 9355.188, 'twoHundredDayAverage': 8306.178, 'currency': 'TRY', 'exchange': 'IST', 'quoteType': 'INDEX', 'symbol': 'XU100.IS',
        'underlyingSymbol': 'XU100.IS', 'shortName': 'BIST 100', 'longName': 'BIST 100', 'firstTradeDateEpochUtc': 867738600, 'timeZoneFullName': 'Europe/Istanbul',
          'timeZoneShortName': 'TRT', 'uuid': 'edf9dd2c-49a2-3d52-8fcf-10d8f1d9835e', 'messageBoardId': 'finmb_INDEXXU100.IS', 'gmtOffSetMilliseconds': 10800000, 
          'trailingPegRatio': None}


"""{'address1': 'Mehmet Akif Ersoy Mahallesi Istiklal',
 'address2': 'Marsi Caddesi No: 16 Yenimahalle',
   'city': 'Ankara', 'zip': '06200', 'country': 'Turkey',
     'phone': '90 312 592 60 00', 'fax': '90 312 354 13 02', 'website': 'https://www.aselsan.com', 'industry': 'Aerospace & Defense',
       'industryKey': 'aerospace-defense', 'industryDisp': 'Aerospace & Defense', 'sector': 'Industrials', 'sectorKey': 'industrials',
        'sectorDisp': 'Industrials', 'longBusinessSummary': 'ASELSAN Elektronik Sanayi ve Ticaret Anonim Sirketi engages in the research,
       development, engineering, production, testing, assembly, integration, sale, after sales support, consultancy, and trading of software,
         equipment, systems, tools, materials, and platforms. It operates through five divisions: Communication and Information Technologies;
           Radar and Electronic Warfare Systems; Defense Systems Technologies; Microelectronics, Guidance & Electro-Optics; and Transportation, Security,
             Energy, Automation and Medical Systems. The company offers communication and information technologies, radar and electronic warfare, electro-optics, avionics, 
             unmanned systems, air defense and missile systems, and command and control systems; transportation, security, traffic, automation, and medical systems; and land, naval, 
             and weapon systems. It offers its products and services for army, navy, air force, and aerospace applications in Turkey and internationally. 
             The company was founded in 1975 and is based in Ankara, Türkiye with facilities in Ankara and Istanbul, Türkiye. ASELSAN Elektronik Sanayi ve Ticaret Anonim Sirketi operates 
             as a subsidiary of Turkish Armed Forces Foundation.', 'fullTimeEmployees': 11454, 'companyOfficers': [{'maxAge': 1, 'name': 'Mr. Ahmet  Akyol', 'age': 40, 
             'title': 'Chief Executive Officer', 'yearBorn': 1982, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Mr. Yunus  Poyraz', 'age': 39, 'title': 'VP & CFO',
               'yearBorn': 1983, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Mr. Taha  Yucel', 'age': 51, 'title': '?Vice President of Technology & Strategy',
                 'yearBorn': 1971, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Pinar  Celebi', 'title': 'Investor Relations & Enterprise Risk Manager', 
                 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Mr. Mustafa  Yaman', 'age': 47, 'title': 'Vice President of Communication & Information Technologies',
                   'yearBorn': 1975, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Mr. Osman Devrim Fidanci', 'age': 46, 
                   'title': 'Vice President of Business Development & Marketing', 'yearBorn': 1976, 'exercisedValue': 0, 'unexercisedValue': 0}], 'maxAge': 86400, 'priceHint': 2,
                     'previousClose': 44.78, 
                     'open': 44.96, 
                     'dayLow': 44.26, 
                     'dayHigh': 45.32, 
                     'regularMarketPreviousClose': 44.78, 
                     'regularMarketOpen': 44.96, 
                     'regularMarketDayLow': 44.26,
                     'regularMarketDayHigh': 45.32, 
                     'dividendRate': 0.09, 'dividendYield': 0.002, 'exDividendDate': 1700611200, 'payoutRatio': 0.028900001, 'fiveYearAvgDividendYield': 0.58,'beta': 0.668, 'trailingPE': 12.888252, 
  
  'volume': 36849927, 'regularMarketVolume': 36849927, 'averageVolume': 60106906, 'averageVolume10days': 41622267,
     'averageDailyVolume10Day': 41622267, 'bid': 44.96, 'ask': 44.4, 'bidSize': 0, 'askSize': 0, 
     'marketCap': 205108805632, 
     'fiftyTwoWeekLow': 19.39, 
'fiftyTwoWeekHigh': 50.4, 
'priceToSalesTrailing12Months': 4.1335897, 
'fiftyDayAverage': 44.86, 'twoHundredDayAverage': 35.089825,

 'trailingAnnualDividendRate': 0.088, 'trailingAnnualDividendYield': 0.001965163, 'currency': 'TRY', 
 'enterpriseValue': 220132704256, 'profitMargins': 0.32094002,
  'floatShares': 1176708000, 'sharesOutstanding': 4560000000, 'heldPercentInsiders': 0.74195, 'heldPercentInstitutions': 0.03965, 
 
 'impliedSharesOutstanding': 4761999872, 
 'bookValue': 10.751, 'priceToBook': 4.183797, 
 'lastFiscalYearEnd': 1672444800, 'nextFiscalYearEnd': 1703980800,
 'mostRecentQuarter': 1696032000, 'earningsQuarterlyGrowth': 1.243, 'netIncomeToCommon': 15924861952, 'trailingEps': 3.49, 'lastSplitFactor': '200:100', 
  'lastSplitDate': 1692921600, 'enterpriseToRevenue': 4.436, 'enterpriseToEbitda': 103.389, 
  '52WeekChange': 0.39256966, 'SandP52WeekChange': 0.24729478,
 'lastDividendValue': 0.087719, 'lastDividendDate': 1700611200, 
 'gmtOffSetMilliseconds': 10800000, 'currentPrice': 44.98, 'targetHighPrice': 59.32, 'targetLowPrice': 41.0, 'targetMeanPrice': 51.91, 
   'targetMedianPrice': 54.5, 'recommendationMean': 2.4, 'recommendationKey': 'buy', 'numberOfAnalystOpinions': 10, 'totalCash': 1727102976, 
       'totalCashPerShare': 0.379, 
       'ebitda': 2129174016, 'totalDebt': 16465266688, 'quickRatio': 0.573, 'currentRatio': 1.254, 'totalRevenue': 49620021248, 
       'debtToEquity': 33.391, 'revenuePerShare': 10.882, 'returnOnAssets': 0.01008, 'returnOnEquity': 0.3977, 'grossProfits': 11783455000, 
   'freeCashflow': -16708858880, 'operatingCashflow': 5283073024, 'earningsGrowth': 1.243, 'revenueGrowth': 1.033, 'grossMargins': 0.31943,
     'ebitdaMargins': 0.04291, 'operatingMargins': 0.19058001"""