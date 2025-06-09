import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#sektor_list = [XUSIN.IS, XUHIZ.IS, XUMAL.IS, XUTEK.IS, XBANK.IS, XAKUR.IS, XBSLM.IS, XELKT.IS, XFINK.IS, XGMYO.IS, XGIDA.IS, XHOLD.IS, XILTM.IS, XINSA.IS, 
#               XKAGT.IS, XKMYA.IS, XMADN.IS, XYORT.IS, XMANA.IS, XMESY.IS, XSGRT.IS, XSPOR.IS, XTAST.IS, XTEKS.IS, XTCRT.IS, XTRZM.IS, XULAS.IS] 

#Just change the stock code 
stocknameone  ="XGIDA.IS"
stocknametwo  ="MGROS.IS"
stocknamethree="BIMAS.IS"
stocknamefour ="SOKM.IS"
stocknamefive ="USDTRY=X"
stocknamesix  ="BIMAS.IS"
#do not forget change the date
start_date = "2023-09-01"
end_date   = "2023-11-25"

stock_one   = yf.download(stocknameone,start=start_date,end=end_date)
stock_two   = yf.download(stocknametwo,start=start_date,end=end_date)
stock_three = yf.download(stocknamethree,start=start_date,end=end_date)
stock_four  = yf.download(stocknamefour,start=start_date,end=end_date)
stock_five  = yf.download(stocknamefive,start=start_date,end=end_date)
stock_six   = yf.download(stocknamesix,start=start_date,end=end_date)

fig, axes = plt.subplots(3, 2, figsize=(15, 9))

axes[0,0].plot(stock_one['Close'])
axes[0,0].set_title(stocknameone)

axes[0,1].plot(stock_two['Close'])
axes[0,1].set_title(stocknametwo)

axes[1,0].plot(stock_three['Close'])
axes[1,0].set_title(stocknamethree)

axes[1,1].plot(stock_four['Close'])
axes[1,1].set_title(stocknamefour)

axes[2,0].plot(stock_five['Close'])
axes[2,0].set_title(stocknamefive)

axes[2,1].plot(stock_six['Close'])
axes[2,1].set_title(stocknamesix)
print(stock_six)
plt.tight_layout()
plt.show()