# Stock Analysis & Backtesting Tool

A comprehensive Python tool for technical analysis of stocks with support for Turkish (BIST) and international markets. This tool downloads historical data, calculates multiple technical indicators, and saves results for backtesting purposes.

## Features

### Technical Indicators Calculated
- **Trend Indicators**: RSI, ADX, MACD, ROC, EMA, Supertrend, Ichimoku Cloud
- **Volume Indicators**: OBV, CMF, AD, MFI, VWAP
- **Volatility Indicators**: ATR, Bollinger Bands
- **Momentum Indicators**: CCI, Stochastic, StochRSI
- **Custom Indicators**: FWMA, KAMA
- **Derived Metrics**: Year-to-date percentage, trend analysis, cloud position analysis

### Key Capabilities
- Single stock analysis with comprehensive technical indicators
- Bulk analysis of multiple stocks (portfolios, indices)
- Automatic CSV export with timestamps
- Turkish stock market support (BIST stocks with .IS suffix)
- Flexible time periods (1y, 2y, 5y, max)
- Real-time data from Yahoo Finance

## Installation

### Prerequisites
```bash
pip install yfinance pandas matplotlib pandas-ta numpy
```

### Required Libraries
- `yfinance` - Yahoo Finance data download
- `pandas` - Data manipulation and analysis
- `matplotlib` - Plotting (for future visualization)
- `pandas-ta` - Technical analysis indicators
- `numpy` - Numerical computations

## Usage

### Single Stock Analysis
```python
# Analyze a single stock for 2 years
data = single_stock_analysis("AAPL", period="2y")

# Turkish stock example
data = single_stock_analysis("SAHOL.IS", period="5y")

# Get maximum available historical data
data = single_stock_analysis("MGROS.IS", period="max")
```

### Multiple Stocks Analysis
```python
# Define your stock list
my_portfolio = ["AAPL", "GOOGL", "MSFT"]
turkish_stocks = ["SAHOL.IS", "THYAO.IS", "KCHOL.IS"]

# Analyze multiple stocks
results = analyze_multiple_stocks(my_portfolio, period="2y")
```

### Pre-defined Stock Lists
The code includes two pre-defined Turkish stock lists:
- **Portfolio**: 11 selected Turkish stocks
- **BIST100**: Complete BIST 100 index stocks (100 stocks)

## Output

### CSV Files
- Automatically saved to `Backtesting_CSVs/` directory
- Filename format: `{SYMBOL}_{PERIOD}_{DD_MM_YY}.csv`
- Contains all OHLCV data + calculated indicators

### Console Output
- Download progress and processing status
- Latest values summary for each stock:
  - Current price, RSI, ADX, MACD
  - Ichimoku cloud position and TK cross signals
  - Trend direction and Supertrend signals

## Technical Indicators Explained

### Trend Analysis
- **TrendWay**: Combines ADX and ROC to determine trend direction
  - "upper": Strong uptrend (ADX > 20, ROC > 0)
  - "lower": Strong downtrend (ADX > 20, ROC ≤ 0)
  - "no-trend": Sideways movement (ADX ≤ 20)

### Ichimoku Cloud Analysis
- **Cloud_Position**: Price position relative to Senkou spans
  - "Above_Cloud": Bullish zone
  - "Below_Cloud": Bearish zone
- **TK_Cross**: Tenkan-Kijun cross signals
  - "Bullish": Tenkan > Kijun
  - "Bearish": Tenkan < Kijun

### Custom Metrics
- **YF%**: Year-to-date percentage performance
- **BB_Pot**: Bollinger Band upper potential (upside %)
- **BB_Opt**: Bollinger Band lower potential (downside %)
- **MACDAS**: MACD Accelerator Signal (MACD - Signal)

## Stock Symbol Formats

### International Stocks
```python
"AAPL"    # Apple Inc.
"GOOGL"   # Alphabet Inc.
"MSFT"    # Microsoft
```

### Turkish Stocks (BIST)
```python
"SAHOL.IS"  # Sabancı Holding
"THYAO.IS"  # Türk Hava Yolları
"KCHOL.IS"  # Koç Holding
```

## Time Periods
- `"1y"` - 1 year of data
- `"2y"` - 2 years of data
- `"5y"` - 5 years of data
- `"max"` - Maximum available historical data

## Example Usage

### Basic Analysis
```python
# Run the script as-is to analyze BIST100 stocks
python stock_analysis.py

# Or modify the main section for your needs:
if __name__ == "__main__":
    # Single stock analysis
    apple_data = single_stock_analysis("AAPL", period="2y")
    
    # Portfolio analysis
    my_stocks = ["AAPL", "GOOGL", "TSLA"]
    results = analyze_multiple_stocks(my_stocks, period="1y")
```

### Working with Results
```python
# Access the returned DataFrame
data = single_stock_analysis("AAPL", period="1y")
if data is not None:
    # Latest RSI value
    current_rsi = data.iloc[-1]['RSI']
    
    # Filter for specific conditions
    oversold = data[data['RSI'] < 30]
    
    # Export to different format
    data.to_excel('AAPL_analysis.xlsx')
```

## Error Handling

The tool includes comprehensive error handling:
- Invalid stock symbols are skipped with error messages
- Network issues are handled gracefully
- Missing data scenarios are managed
- Warnings are suppressed for cleaner output

## File Structure
```
project/
├── stock_analysis.py          # Main analysis script
├── Backtesting_CSVs/         # Auto-created directory for CSV outputs
│   ├── AAPL_2y_22_07_25.csv
│   ├── SAHOL.IS_max_22_07_25.csv
│   └── ...
└── README.md                 # This file
```

## Performance Notes

- API delay of 1 second between stocks to avoid rate limiting
- Processing time varies with data amount and indicators calculated
- Large datasets (max period) may take longer to process
- CSV files can become large for extended periods

## Troubleshooting

### Common Issues
1. **"No data found"**: Check stock symbol spelling and market availability
2. **Network errors**: Ensure stable internet connection
3. **Missing indicators**: Some indicators require minimum data points
4. **Permission errors**: Ensure write access to create CSV directory

### Tips
- Use `.IS` suffix for Turkish stocks
- Start with shorter periods for testing
- Check Yahoo Finance directly if symbols don't work
- Monitor console output for processing progress

## Future Enhancements

Potential additions for backtesting functionality:
- Strategy implementation framework
- Performance metrics calculation
- Visualization tools
- Portfolio optimization
- Risk management indicators

## Contributing

Feel free to extend this tool with:
- Additional technical indicators
- New market support
- Strategy backtesting features
- Performance visualizations
- Risk metrics

## License

This tool is for educational and research purposes. Please ensure compliance with data provider terms of service.