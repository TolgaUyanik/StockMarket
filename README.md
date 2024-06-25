# StockMarket

This project is a stock market analysis tool designed to analyze stocks listed on the BIST100 (XU100.IS) index using the `yfinance` and `pandas` libraries. The script fetches stock data, processes it, and generates CSV files for stocks recommended for buying, holding, and selling based on various metrics.

## Features

- Fetches stock data for all BIST100 companies.
- Computes various metrics such as price-to-book ratio, potential gain, and how far the current price is from target prices.
- Generates recommendations for buying, holding, and selling stocks.
- Creates CSV files for easy analysis and further processing.

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/TolgaUyanik/StockMarket
    ```
2. Navigate to the project directory:
    ```bash
    cd StockMarket
    ```
3. Install the required packages:
    ```bash
    pip install yfinance pandas
    ```

## Usage

Run the script to perform market analysis:
```bash
python Stock_Analysis.py
 ```
##The script will output the following CSV files in the project directory:

- buy_list.csv: List of stocks recommended for buying.
- hold_list.csv: List of stocks recommended for holding.
- sell_list.csv: List of stocks recommended for selling.
- Day_Trading.csv: List of stocks with significant daily changes, suitable for day trading.
- Script Details
- market_analysis function
- This function performs the following tasks:

- Fetch Stock Data: Retrieves data for each stock in the BIST100 index.
- Data Processing: Computes metrics such as:
- change: Percentage change from opening price to current price.
- net_change: Absolute value of change.
- Daily Max Change: Maximum daily change.
- How Far Median: Difference between current price and target median price.
- Other metrics related to target high, low, and mean prices.
- Recommendations: Based on the computed metrics, stocks are categorized into buy, hold, and sell lists.
- CSV Generation: Saves the categorized lists into CSV files for further analysis.

## Key Metrics

- Price-to-Book Ratio: A valuation ratio comparing the current price to the book value.
- Potential: Potential gain from the target high price.
- Under Median: How far the current price is below the target median price.
- How Close to Target Low Price: Proximity of the current price to the target low price.
- Daily Max Change: Intraday price volatility.

## Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for more details
