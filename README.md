# Stock Market Technical Analysis Tool

This project provides a comprehensive stock market analysis tool that uses various technical indicators to identify potential trading opportunities.

## Technical Indicators Explained

### 1. RSI (Relative Strength Index)
- **What it measures**: Momentum and overbought/oversold conditions
- **Range**: 0 to 100
- **Interpretation**:
  - RSI < 30: Oversold condition (Potential buy signal)
  - RSI > 70: Overbought condition (Potential sell signal)
  - Values between 30-70: Neutral territory

### 2. ADX (Average Directional Index)
- **What it measures**: Trend strength
- **Range**: 0 to 100
- **Interpretation**:
  - ADX > 20: Indicates a trend is forming
  - ADX < 20: Indicates a weak or non-existent trend
  - Note: ADX doesn't indicate trend direction, only strength

### 3. MACD (Moving Average Convergence Divergence)
- **What it measures**: Trend direction and momentum
- **Components**:
  - MACD Line: Difference between 12 and 26-day EMAs
  - Signal Line: 9-day EMA of MACD Line
- **Interpretation**:
  - MACD > Signal Line: Bullish signal
  - MACD < Signal Line: Bearish signal
  - MACD > 0: Potential buy signal
  - MACD < 0: Potential sell signal

### 4. CCI (Commodity Channel Index)
- **What it measures**: Price deviation from its statistical mean
- **Range**: Typically -100 to +100
- **Interpretation**:
  - CCI < -100: Oversold condition (Buy signal)
  - CCI > 100: Overbought condition (Sell signal)
  - Values between -100 and 100: Neutral territory

### 5. ROC (Rate of Change)
- **What it measures**: Price momentum
- **Interpretation**:
  - ROC > 0: Upward momentum
  - ROC < 0: Downward momentum
  - Higher values indicate stronger momentum

### 6. ATR (Average True Range)
- **What it measures**: Market volatility
- **Interpretation**:
  - Higher ATR: Higher volatility
  - Lower ATR: Lower volatility
  - Useful for:
    - Setting stop-loss levels
    - Determining position sizes
    - Identifying potential trading opportunities in volatile markets

### 7. OBV (On Balance Volume)
- **What it measures**: Volume flow
- **Interpretation**:
  - Rising OBV: Bullish signal (accumulation)
  - Falling OBV: Bearish signal (distribution)
  - Confirms price trends through volume analysis

### 8. Bollinger Bands (%B)
- **What it measures**: Price relative to volatility bands
- **Components**:
  - Middle Band: 20-day SMA
  - Upper Band: Middle Band + (2 * Standard Deviation)
  - Lower Band: Middle Band - (2 * Standard Deviation)
- **Interpretation**:
  - %B < 0.4: Price near lower band (Potential oversold)
  - %B > 0.6: Price near upper band (Potential overbought)

## Best Practices

1. Always use multiple indicators for confirmation
2. Consider the overall market trend
3. Use ATR to manage risk appropriately
4. Monitor volume (OBV) for trend confirmation
5. Combine technical analysis with fundamental analysis for better results

## Note

This tool is designed to assist in technical analysis but should not be used as the sole basis for trading decisions. Always conduct thorough research and consider multiple factors before making investment decisions.