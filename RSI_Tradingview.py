import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
import warnings
warnings.filterwarnings('ignore')

class RSIDivergenceDetector:
    def __init__(self, 
                 rsi_period=14,
                 pivot_lookback_left=5,
                 pivot_lookback_right=5,
                 range_lower=5,
                 range_upper=60,
                 plot_bull=True,
                 plot_hidden_bull=False,
                 plot_bear=True,
                 plot_hidden_bear=False):
        
        self.rsi_period = rsi_period
        self.pivot_lookback_left = pivot_lookback_left
        self.pivot_lookback_right = pivot_lookback_right
        self.range_lower = range_lower
        self.range_upper = range_upper
        self.plot_bull = plot_bull
        self.plot_hidden_bull = plot_hidden_bull
        self.plot_bear = plot_bear
        self.plot_hidden_bear = plot_hidden_bear
        
    def calculate_rsi(self, prices):
        """Calculate RSI using the standard formula"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.rsi_period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def find_pivots(self, data, order):
        """Find pivot highs and lows"""
        highs = argrelextrema(data.values, np.greater, order=order)[0]
        lows = argrelextrema(data.values, np.less, order=order)[0]
        return highs, lows
    
    def is_in_range(self, current_idx, pivot_idx):
        """Check if pivot is within specified range"""
        bars_since = current_idx - pivot_idx
        return self.range_lower <= bars_since <= self.range_upper
    
    def detect_divergences(self, df):
        """Main function to detect all types of divergences"""
        # Calculate RSI
        df['RSI'] = self.calculate_rsi(df['Close'])
        
        # Find pivots
        rsi_highs, rsi_lows = self.find_pivots(df['RSI'], self.pivot_lookback_left)
        price_highs, price_lows = self.find_pivots(df['High'], self.pivot_lookback_left)
        
        # Initialize divergence columns
        df['regular_bullish'] = False
        df['hidden_bullish'] = False
        df['regular_bearish'] = False
        df['hidden_bearish'] = False
        
        # Regular Bullish Divergence Detection
        if self.plot_bull:
            self._detect_regular_bullish(df, rsi_lows, price_lows)
        
        # Hidden Bullish Divergence Detection
        if self.plot_hidden_bull:
            self._detect_hidden_bullish(df, rsi_lows, price_lows)
        
        # Regular Bearish Divergence Detection
        if self.plot_bear:
            self._detect_regular_bearish(df, rsi_highs, price_highs)
        
        # Hidden Bearish Divergence Detection
        if self.plot_hidden_bear:
            self._detect_hidden_bearish(df, rsi_highs, price_highs)
        
        return df
    
    def _detect_regular_bullish(self, df, rsi_lows, price_lows):
        """Detect regular bullish divergences"""
        for i in range(1, len(rsi_lows)):
            current_idx = rsi_lows[i]
            prev_idx = rsi_lows[i-1]
            
            if not self.is_in_range(current_idx, prev_idx):
                continue
            
            # RSI Higher Low
            rsi_hl = df['RSI'].iloc[current_idx] > df['RSI'].iloc[prev_idx]
            
            # Price Lower Low (find corresponding price lows)
            current_price_low = df['Low'].iloc[current_idx]
            prev_price_low = df['Low'].iloc[prev_idx]
            price_ll = current_price_low < prev_price_low
            
            if rsi_hl and price_ll:
                df.loc[df.index[current_idx], 'regular_bullish'] = True
    
    def _detect_hidden_bullish(self, df, rsi_lows, price_lows):
        """Detect hidden bullish divergences"""
        for i in range(1, len(rsi_lows)):
            current_idx = rsi_lows[i]
            prev_idx = rsi_lows[i-1]
            
            if not self.is_in_range(current_idx, prev_idx):
                continue
            
            # RSI Lower Low
            rsi_ll = df['RSI'].iloc[current_idx] < df['RSI'].iloc[prev_idx]
            
            # Price Higher Low
            current_price_low = df['Low'].iloc[current_idx]
            prev_price_low = df['Low'].iloc[prev_idx]
            price_hl = current_price_low > prev_price_low
            
            if rsi_ll and price_hl:
                df.loc[df.index[current_idx], 'hidden_bullish'] = True
    
    def _detect_regular_bearish(self, df, rsi_highs, price_highs):
        """Detect regular bearish divergences"""
        for i in range(1, len(rsi_highs)):
            current_idx = rsi_highs[i]
            prev_idx = rsi_highs[i-1]
            
            if not self.is_in_range(current_idx, prev_idx):
                continue
            
            # RSI Lower High
            rsi_lh = df['RSI'].iloc[current_idx] < df['RSI'].iloc[prev_idx]
            
            # Price Higher High
            current_price_high = df['High'].iloc[current_idx]
            prev_price_high = df['High'].iloc[prev_idx]
            price_hh = current_price_high > prev_price_high
            
            if rsi_lh and price_hh:
                df.loc[df.index[current_idx], 'regular_bearish'] = True
    
    def _detect_hidden_bearish(self, df, rsi_highs, price_highs):
        """Detect hidden bearish divergences"""
        for i in range(1, len(rsi_highs)):
            current_idx = rsi_highs[i]
            prev_idx = rsi_highs[i-1]
            
            if not self.is_in_range(current_idx, prev_idx):
                continue
            
            # RSI Higher High
            rsi_hh = df['RSI'].iloc[current_idx] > df['RSI'].iloc[prev_idx]
            
            # Price Lower High
            current_price_high = df['High'].iloc[current_idx]
            prev_price_high = df['High'].iloc[prev_idx]
            price_lh = current_price_high < prev_price_high
            
            if rsi_hh and price_lh:
                df.loc[df.index[current_idx], 'hidden_bearish'] = True
    
    def plot_results(self, df, symbol):
        """Plot the results with price, RSI, and divergence signals"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12), 
                                       gridspec_kw={'height_ratios': [2, 1]})
        
        # Plot price
        ax1.plot(df.index, df['Close'], label='Close Price', linewidth=1.5)
        
        # Plot divergence signals on price chart
        bull_signals = df[df['regular_bullish']]
        hidden_bull_signals = df[df['hidden_bullish']]
        bear_signals = df[df['regular_bearish']]
        hidden_bear_signals = df[df['hidden_bearish']]
        
        if len(bull_signals) > 0:
            ax1.scatter(bull_signals.index, bull_signals['Low'], 
                       color='green', marker='^', s=100, label='Regular Bullish', zorder=5)
        
        if len(hidden_bull_signals) > 0:
            ax1.scatter(hidden_bull_signals.index, hidden_bull_signals['Low'], 
                       color='lightgreen', marker='^', s=80, label='Hidden Bullish', zorder=5)
        
        if len(bear_signals) > 0:
            ax1.scatter(bear_signals.index, bear_signals['High'], 
                       color='red', marker='v', s=100, label='Regular Bearish', zorder=5)
        
        if len(hidden_bear_signals) > 0:
            ax1.scatter(hidden_bear_signals.index, hidden_bear_signals['High'], 
                       color='lightcoral', marker='v', s=80, label='Hidden Bearish', zorder=5)
        
        ax1.set_title(f'{symbol} - Price Chart with Divergence Signals')
        ax1.set_ylabel('Price')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot RSI
        ax2.plot(df.index, df['RSI'], label='RSI', color='#2962FF', linewidth=2)
        ax2.axhline(y=70, color='gray', linestyle='--', alpha=0.7, label='Overbought (70)')
        ax2.axhline(y=30, color='gray', linestyle='--', alpha=0.7, label='Oversold (30)')
        ax2.axhline(y=50, color='gray', linestyle=':', alpha=0.5, label='Middle Line (50)')
        ax2.fill_between(df.index, 30, 70, alpha=0.1, color='blue')
        
        # Plot divergence signals on RSI chart
        if len(bull_signals) > 0:
            ax2.scatter(bull_signals.index, bull_signals['RSI'], 
                       color='green', marker='^', s=100, zorder=5)
        
        if len(hidden_bull_signals) > 0:
            ax2.scatter(hidden_bull_signals.index, hidden_bull_signals['RSI'], 
                       color='lightgreen', marker='^', s=80, zorder=5)
        
        if len(bear_signals) > 0:
            ax2.scatter(bear_signals.index, bear_signals['RSI'], 
                       color='red', marker='v', s=100, zorder=5)
        
        if len(hidden_bear_signals) > 0:
            ax2.scatter(hidden_bear_signals.index, hidden_bear_signals['RSI'], 
                       color='lightcoral', marker='v', s=80, zorder=5)
        
        ax2.set_title('RSI with Divergence Signals')
        ax2.set_ylabel('RSI')
        ax2.set_xlabel('Date')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(0, 100)
        
        plt.tight_layout()
        plt.show()
    
    def get_divergence_summary(self, df):
        """Get a summary of detected divergences"""
        summary = {
            'Regular Bullish': len(df[df['regular_bullish']]),
            'Hidden Bullish': len(df[df['hidden_bullish']]),
            'Regular Bearish': len(df[df['regular_bearish']]),
            'Hidden Bearish': len(df[df['hidden_bearish']])
        }
        return summary

# Example usage
def analyze_stock(symbol, period='6mo'):
    """Analyze a stock for RSI divergences"""
    # Download data
    stock = yf.Ticker(symbol)
    df = stock.history(period=period, interval="5m")
    
    # Initialize detector
    detector = RSIDivergenceDetector(
        rsi_period=14,
        pivot_lookback_left=5,
        pivot_lookback_right=5,
        range_lower=5,
        range_upper=60,
        plot_bull=True,
        plot_hidden_bull=False,  # Set to True to include hidden divergences
        plot_bear=True,
        plot_hidden_bear=False   # Set to True to include hidden divergences
    )
    
    # Detect divergences
    df_with_divergences = detector.detect_divergences(df)
    
    # Get summary
    summary = detector.get_divergence_summary(df_with_divergences)
    print(f"\nDivergence Summary for {symbol}:")
    for div_type, count in summary.items():
        print(f"{div_type}: {count}")
    
    # Plot results
    detector.plot_results(df_with_divergences, symbol)
    
    # Return recent divergences
    recent_divergences = df_with_divergences[
        (df_with_divergences['regular_bullish']) |
        (df_with_divergences['hidden_bullish']) |
        (df_with_divergences['regular_bearish']) |
        (df_with_divergences['hidden_bearish'])
    ].tail(10)
    
    if len(recent_divergences) > 0:
        print(f"\nRecent divergences for {symbol}:")
        for idx, row in recent_divergences.iterrows():
            div_types = []
            if row['regular_bullish']: div_types.append('Regular Bullish')
            if row['hidden_bullish']: div_types.append('Hidden Bullish')
            if row['regular_bearish']: div_types.append('Regular Bearish')
            if row['hidden_bearish']: div_types.append('Hidden Bearish')
            
            print(f"{idx.strftime('%Y-%m-%d')}: {', '.join(div_types)} - RSI: {row['RSI']:.2f}, Close: ${row['Close']:.2f}")
    
    return df_with_divergences

# Example: Analyze Apple stock
if __name__ == "__main__":
    # Analyze AAPL for the last 6 months
    result = analyze_stock('KCHOL.IS', '1mo')