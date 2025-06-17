# 📊 Technical Indicators Cheat Sheet

> A comprehensive quick-reference guide for technical analysis indicators used in trading and market analysis.

## Table of Contents
- [Momentum Oscillators](#-momentum-oscillators)
- [Trend Indicators](#-trend-indicators)
- [Ichimoku Cloud System](#️-ichimoku-cloud-system)
- [MACD Family](#-macd-family)
- [Volatility Indicators](#-volatility-indicators)
- [Volume Indicators](#-volume-indicators)
- [Quick Signal Reference](#-quick-signal-reference)
- [Trading Combinations](#-trading-combinations)
- [Pro Tips](#-pro-tips)

---

## 🔥 MOMENTUM OSCILLATORS (0-100 Range)

### 📈 **RSI (Relative Strength Index)**
- **Range**: 0-100 | **Period**: 14
- **Overbought**: >70 | **Oversold**: <30
- **Signals**: 
  - Buy: RSI crosses above 30 (exit oversold)
  - Sell: RSI crosses below 70 (exit overbought)
  - Divergence: Price vs RSI direction mismatch
- **Best for**: Ranging markets, momentum confirmation

### 📊 **Stochastic (%K, %D)**
- **Range**: 0-100 | **Periods**: 14,3,3
- **Overbought**: >80 | **Oversold**: <20
- **Signals**:
  - Buy: %K crosses above %D in oversold zone
  - Sell: %K crosses below %D in overbought zone
- **Best for**: Range-bound markets, reversal spots

### 🚀 **StochRSI (K, D)**
- **Range**: 0-100 | **Period**: 14
- **Overbought**: >80 | **Oversold**: <20
- **Signals**: Same as Stochastic but more sensitive
- **Best for**: Early momentum detection, quick reversals

### 💰 **MFI (Money Flow Index)**
- **Range**: 0-100 | **Period**: 14
- **Overbought**: >80 | **Oversold**: <20
- **Signals**: Volume-weighted RSI signals
- **Best for**: Volume confirmation with price

### ⚡ **CCI (Commodity Channel Index)**
- **Range**: Unbounded (typically -100 to +100)
- **Extreme**: >+100 (overbought) | <-100 (oversold)
- **Signals**: 
  - Buy: CCI crosses above -100
  - Sell: CCI crosses below +100
- **Best for**: Cyclical markets, extreme readings

---

## 📈 TREND INDICATORS

### 📊 **ADX (Average Directional Index)**
- **Range**: 0-100 | **Period**: 14
- **Strong Trend**: >25 | **Very Strong**: >50
- **Weak Trend**: <20
- **Signals**: Trend strength only (not direction)
- **Best for**: Confirming trend strength

### 🎯 **Supertrend**
- **Values**: Price levels above/below price
- **Signals**:
  - Buy: Price closes above Supertrend line
  - Sell: Price closes below Supertrend line
- **Best for**: Trend following, stop-loss levels

### 📍 **VWAP (Volume Weighted Average Price)**
- **Values**: Price level
- **Signals**:
  - Bullish: Price above VWAP
  - Bearish: Price below VWAP
- **Best for**: Intraday trading, institutional levels

---

## ☁️ ICHIMOKU CLOUD SYSTEM

### **Five Lines:**
- **Tenkan** (9): Conversion line - short-term momentum
- **Kijun** (26): Base line - medium-term trend
- **Senkou A**: Leading span A (cloud edge)
- **Senkou B**: Leading span B (cloud edge)
- **Chikou**: Lagging span (current close 26 periods back)

### **Key Signals:**
- **TK Cross**: 
  - Bullish: Tenkan crosses above Kijun
  - Bearish: Tenkan crosses below Kijun
- **Cloud Position**:
  - Bullish: Price above cloud
  - Bearish: Price below cloud
  - Neutral: Price in cloud
- **Best for**: Complete trend analysis system

---

## 📊 MACD FAMILY

### **MACD Line**: 12EMA - 26EMA
### **Signal Line**: 9EMA of MACD
### **Histogram**: MACD - Signal

### **Signals:**
- **Bullish**: MACD crosses above Signal line
- **Bearish**: MACD crosses below Signal line
- **Momentum**: Histogram expanding/contracting
- **Divergence**: MACD vs price direction mismatch
- **Best for**: Trend changes, momentum shifts

---

## 💨 VOLATILITY INDICATORS

### 📏 **ATR (Average True Range)**
- **Values**: Price units | **Period**: 14
- **High ATR**: High volatility
- **Low ATR**: Low volatility
- **Best for**: Position sizing, stop-loss distances

### 🎈 **Bollinger Bands**
- **BB Width**: Distance between bands (volatility)
- **%B**: Position within bands (0-100)
- **Signals**:
  - Buy: %B < 0 (below lower band)
  - Sell: %B > 100 (above upper band)
  - Squeeze: BB Width contracting
- **Best for**: Volatility analysis, mean reversion

---

## 📊 VOLUME INDICATORS

### 💧 **CMF (Chaikin Money Flow)**
- **Range**: -1 to +1 | **Period**: 20
- **Bullish**: CMF > 0
- **Bearish**: CMF < 0
- **Strong**: |CMF| > 0.25
- **Best for**: Volume-price relationship

---

## 🚨 QUICK SIGNAL REFERENCE

| Indicator | Buy Signal | Sell Signal | Overbought | Oversold |
|-----------|------------|-------------|------------|----------|
| **RSI** | Cross > 30 | Cross < 70 | > 70 | < 30 |
| **Stoch** | %K > %D in < 20 | %K < %D in > 80 | > 80 | < 20 |
| **StochRSI** | Cross > 20 | Cross < 80 | > 80 | < 20 |
| **MFI** | Cross > 20 | Cross < 80 | > 80 | < 20 |
| **CCI** | Cross > -100 | Cross < 100 | > 100 | < -100 |
| **MACD** | Line > Signal | Line < Signal | - | - |
| **ADX** | Trend strength | Trend strength | - | - |

---

## ⚡ TRADING COMBINATIONS

### **🎯 Trend Following Combo**
```
ADX > 25 + Supertrend + MACD alignment
```

### **🔄 Mean Reversion Combo**
```
RSI < 30 + %B < 0 + StochRSI oversold
```

### **📈 Momentum Breakout Combo**
```
RSI > 50 + MACD cross + ADX rising
```

### **☁️ Ichimoku Complete Setup**
```
Price > Cloud + TK Cross + Chikou clear
```

---

## 💡 PRO TIPS

### **⏰ Timeframe Rules**
- **Scalping (1-5min)**: StochRSI, CCI
- **Day Trading (15-60min)**: RSI, MACD, Stoch
- **Swing Trading (4H-Daily)**: ADX, Ichimoku, BB
- **Position Trading (Weekly+)**: Long-period RSI, MACD

### **🎨 Market Conditions**
- **Trending**: ADX, Supertrend, MACD, Ichimoku
- **Ranging**: RSI, Stochastic, Bollinger Bands
- **High Volatility**: ATR, Bollinger Width
- **Low Volume**: MFI, CMF for confirmation

### **🚫 Common Mistakes**
- Don't use oscillators alone in strong trends
- Don't ignore divergences
- Don't over-optimize parameters
- Don't use too many indicators at once
- Always combine with price action

### **✅ Best Practices**
- Start with 2-3 indicators maximum
- Confirm signals across timeframes  
- Wait for multiple confirmations
- Use proper risk management
- Backtest your combinations

---

## 📱 Quick Mobile Reference

**🟢 BULLISH SETUP**
```
RSI > 50 + MACD > Signal + Price > VWAP + ADX > 25
```

**🔴 BEARISH SETUP**  
```
RSI < 50 + MACD < Signal + Price < VWAP + ADX > 25
```

**⚠️ NEUTRAL/CAUTION**
```
Oscillators in neutral zone + Low ADX + Price in BB middle
```

---


## 📈 Contributing

Feel free to contribute by:
- Adding new indicators
- Improving signal descriptions
- Sharing trading combinations
- Reporting issues or suggestions

---

## ⚠️ Disclaimer

This cheat sheet is for educational purposes only. Technical indicators should not be used as the sole basis for trading decisions. Always:
- Use proper risk management
- Combine multiple analysis methods
- Backtest strategies before live trading
- Consider fundamental analysis
- Never risk more than you can afford to lose

---

## 📝 License

This guide is open-source and available under the MIT License.

---

**Last Updated**: June 2025  
**Version**: 1.0