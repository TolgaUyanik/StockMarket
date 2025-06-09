import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

Sectors : ("XU100.IS","XU050.IS","XU030.IS","XU500.IS","XLBNK.IS","X10XB.IS","XUTUM.IS","XYUZO.IS","XTUMY.IS","XYLDZ.IS","XBANA.IS","XHARZ.IS","XKOBI.IS","XTMTU.IS",
           "XTM25.IS","XKURY.IS","XUSRD.IS","XSD25.IS","XUSIN.IS","XGIDA.IS","XKMYA.IS","XMADN.IS","XMANA.IS","XMESY.IS","XKAGT.IS","XTAST.IS","XTEKS.IS","XUHIZ.IS",
           "XELKT.IS","XILTM.IS","XINSA.IS","XSPOR.IS","XTCRT.IS","XTRZM.IS","XULAS.IS","XUMAL.IS","XBANK.IS","XSGRT.IS","XFINK.IS","XHOLD.IS","XGMYO.IS","XAKUR.IS",
           "XYORT.IS","XUTEK.IS","XBLSM.IS","XKTUM.IS","XK100.IS","XK050.IS","XK030.IS","XKTMT.IS","XSRDK.IS","XUGRA.IS")

# Define the sector ETF symbols
tech_symbol = "XLK"
healthcare_symbol = "XLV"

# Download historical data for the sectors
tech_data = yf.download("XKAGT.IS",interval="1d",period="1mo")
healthcare_data = yf.download("XELKT.IS", interval="1d",period="1mo")

# Create a DataFrame with the closing prices of both sectors
data = pd.DataFrame({
    'Technology': tech_data['Close'],
    'Healthcare': healthcare_data['Close']
})

# Calculate the percentage change to represent returns
returns = data.pct_change()

# Define a simple rotation strategy: switch to the sector with the higher return
data['Rotation Signal'] = 0  # 0 means hold, 1 means switch to Technology, -1 means switch to Healthcare

data.loc[returns['Technology'] > returns['Healthcare'], 'Rotation Signal'] = 1
data.loc[returns['Technology'] < returns['Healthcare'], 'Rotation Signal'] = -1

# Plot the sector prices and rotation signals
plt.figure(figsize=(12, 6))
plt.plot(data['Technology'], label='Technology', alpha=0.5)
plt.plot(data['Healthcare'], label='Healthcare', alpha=0.5)

# Plot buy signals
plt.plot(data[data['Rotation Signal'] == 1].index,
         data['Technology'][data['Rotation Signal'] == 1],
         '^', markersize=10, color='g', label='Switch to Technology')

# Plot sell signals
plt.plot(data[data['Rotation Signal'] == -1].index,
         data['Healthcare'][data['Rotation Signal'] == -1],
         'v', markersize=10, color='r', label='Switch to Healthcare')

plt.title('Sector Rotation Strategy: Technology and Healthcare')
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.legend()
plt.show()