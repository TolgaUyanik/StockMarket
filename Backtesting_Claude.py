from backtesting import Backtest, Strategy
import pandas as pd
import numpy as np
import yfinance as yf
import pandas_ta as ta
from datetime import datetime
from abc import ABC, abstractmethod

# =============================================================================
# BASE STRATEGY CLASS (Common functionality)
# =============================================================================

class BaseStrategy(Strategy):
    """Base strategy class with common indicators and utilities"""
    
    def __init__(self, broker, data, params):
        super().__init__(broker, data, params)
        # Common parameters that all strategies can use
        self.rsi_period = getattr(self, 'rsi_period', 14)
        self.ma_period = getattr(self, 'ma_period', 20)
        self.atr_period = getattr(self, 'atr_period', 14)
    
    def setup_common_indicators(self):
        """Setup indicators used across multiple strategies"""
        close = pd.Series(self.data.Close, index=self.data.index)
        high = pd.Series(self.data.High, index=self.data.index)
        low = pd.Series(self.data.Low, index=self.data.index)
        volume = pd.Series(self.data.Volume, index=self.data.index)
        
        # Basic indicators
        self.rsi = self.I(ta.rsi, close, length=self.rsi_period)
        self.sma = self.I(ta.sma, close, length=self.ma_period)
        self.atr = self.I(ta.atr, high, low, close, length=self.atr_period)
        
        return close, high, low, volume
    
    def is_valid_signal(self, *indicators):
        """Check if all indicators have valid values"""
        return all(len(ind) > 0 for ind in indicators if ind is not None)

# =============================================================================
# STRATEGY CATEGORIES
# =============================================================================

# 1. TREND FOLLOWING STRATEGIES
class TrendFollowingStrategy(BaseStrategy):
    """Strategy focused on trend following"""
    
    # Strategy parameters
    adx_threshold = 25
    ma_fast = 10
    ma_slow = 30
    
    def init(self):
        close, high, low, volume = self.setup_common_indicators()
        
        # Trend indicators
        self.ma_fast = self.I(ta.sma, close, length=self.ma_fast)
        self.ma_slow = self.I(ta.sma, close, length=self.ma_slow)
        
        def get_adx(high, low, close):
            adx_data = ta.adx(high, low, close, length=14)
            return adx_data.iloc[:, 0]
        self.adx = self.I(get_adx, high, low, close)
        
        def get_supertrend_direction(high, low, close):
            st_data = ta.supertrend(high, low, close, length=10, multiplier=3)
            return st_data.iloc[:, 1]
        self.supertrend_dir = self.I(get_supertrend_direction, high, low, close)
    
    def next(self):
        if not self.position:
            # Buy when fast MA crosses above slow MA and strong trend
            if (self.is_valid_signal(self.ma_fast, self.ma_slow, self.adx, self.supertrend_dir) and
                self.ma_fast[-1] > self.ma_slow[-1] and
                self.adx[-1] > self.adx_threshold and
                self.supertrend_dir[-1] == 1):
                self.buy()
        else:
            # Sell when trend reverses
            if (self.is_valid_signal(self.ma_fast, self.ma_slow, self.supertrend_dir) and
                (self.ma_fast[-1] < self.ma_slow[-1] or self.supertrend_dir[-1] == -1)):
                self.sell()

class MomentumStrategy(BaseStrategy):
    """Strategy focused on momentum indicators"""
    
    # Strategy parameters
    rsi_oversold = 30
    rsi_overbought = 70
    stoch_oversold = 20
    stoch_overbought = 80
    
    def init(self):
        close, high, low, volume = self.setup_common_indicators()
        
        # Momentum indicators
        def get_stoch_k(high, low, close):
            stoch_data = ta.stoch(high, low, close, k=14, d=3)
            return stoch_data.iloc[:, 0]
        
        def get_stoch_d(high, low, close):
            stoch_data = ta.stoch(high, low, close, k=14, d=3)
            return stoch_data.iloc[:, 1]
        
        self.stoch_k = self.I(get_stoch_k, high, low, close)
        self.stoch_d = self.I(get_stoch_d, high, low, close)
        self.mfi = self.I(ta.mfi, high, low, close, volume, length=14)
    
    def next(self):
        if not self.position:
            # Buy on oversold conditions
            if (self.is_valid_signal(self.rsi, self.stoch_k, self.mfi) and
                self.rsi[-1] < self.rsi_oversold and
                self.stoch_k[-1] < self.stoch_oversold and
                self.mfi[-1] < 25):
                self.buy()
        else:
            # Sell on overbought conditions
            if (self.is_valid_signal(self.rsi, self.stoch_k, self.mfi) and
                (self.rsi[-1] > self.rsi_overbought or
                 self.stoch_k[-1] > self.stoch_overbought or
                 self.mfi[-1] > 75)):
                self.sell()

class MeanReversionStrategy(BaseStrategy):
    """Strategy focused on mean reversion"""
    
    # Strategy parameters
    bb_std = 2
    bb_period = 20
    rsi_extreme_oversold = 25
    rsi_extreme_overbought = 75
    
    def init(self):
        close, high, low, volume = self.setup_common_indicators()
        
        # Mean reversion indicators
        def get_bb_lower(close):
            bb_data = ta.bbands(close, length=self.bb_period, std=self.bb_std)
            return bb_data.iloc[:, 0]
        
        def get_bb_upper(close):
            bb_data = ta.bbands(close, length=self.bb_period, std=self.bb_std)
            return bb_data.iloc[:, 2]
        
        def get_bb_percent(close):
            bb_data = ta.bbands(close, length=self.bb_period, std=self.bb_std)
            return bb_data.iloc[:, 4]
        
        self.bb_lower = self.I(get_bb_lower, close)
        self.bb_upper = self.I(get_bb_upper, close)
        self.bb_percent = self.I(get_bb_percent, close)
    
    def next(self):
        if not self.position:
            # Buy when price touches lower Bollinger Band and RSI oversold
            if (self.is_valid_signal(self.bb_percent, self.rsi) and
                self.bb_percent[-1] < 0.1 and
                self.rsi[-1] < self.rsi_extreme_oversold):
                self.buy()
        else:
            # Sell when price touches upper Bollinger Band or RSI overbought
            if (self.is_valid_signal(self.bb_percent, self.rsi) and
                (self.bb_percent[-1] > 0.9 or self.rsi[-1] > self.rsi_extreme_overbought)):
                self.sell()

# 2. COMPLEX MULTI-SIGNAL STRATEGIES
class ConservativeStrategy(BaseStrategy):
    """Conservative strategy requiring multiple confirmations"""
    
    min_buy_signals = 4
    min_sell_signals = 2
    
    def init(self):
        close, high, low, volume = self.setup_common_indicators()
        
        # Multiple indicators for confirmation
        self.mfi = self.I(ta.mfi, high, low, close, volume, length=14)
        self.cci = self.I(ta.cci, high, low, close, length=20)
        
        def get_macd_signal(close):
            macd_data = ta.macd(close, fast=12, slow=26, signal=9)
            return macd_data.iloc[:, 0] > macd_data.iloc[:, 1]  # MACD > Signal
        
        self.macd_bullish = self.I(get_macd_signal, close)
        
        def get_bb_percent(close):
            bb_data = ta.bbands(close, length=20, std=2)
            return bb_data.iloc[:, 4]
        
        self.bb_percent = self.I(get_bb_percent, close)
    
    def count_buy_signals(self):
        """Count bullish signals"""
        signals = 0
        if self.is_valid_signal(self.rsi) and self.rsi[-1] < 35:
            signals += 1
        if self.is_valid_signal(self.mfi) and self.mfi[-1] < 30:
            signals += 1
        if self.is_valid_signal(self.cci) and self.cci[-1] < -100:
            signals += 1
        if self.is_valid_signal(self.macd_bullish) and self.macd_bullish[-1]:
            signals += 1
        if self.is_valid_signal(self.bb_percent) and self.bb_percent[-1] < 0.2:
            signals += 1
        return signals
    
    def count_sell_signals(self):
        """Count bearish signals"""
        signals = 0
        if self.is_valid_signal(self.rsi) and self.rsi[-1] > 65:
            signals += 1
        if self.is_valid_signal(self.mfi) and self.mfi[-1] > 70:
            signals += 1
        if self.is_valid_signal(self.cci) and self.cci[-1] > 100:
            signals += 1
        if self.is_valid_signal(self.bb_percent) and self.bb_percent[-1] > 0.8:
            signals += 1
        return signals
    
    def next(self):
        if not self.position:
            if self.count_buy_signals() >= self.min_buy_signals:
                self.buy()
        else:
            if self.count_sell_signals() >= self.min_sell_signals:
                self.sell()

class AggressiveStrategy(BaseStrategy):
    """Aggressive strategy with quick entries/exits"""
    
    def init(self):
        close, high, low, volume = self.setup_common_indicators()
        
        # Fast indicators
        self.rsi_fast = self.I(ta.rsi, close, length=9)
        self.ema_fast = self.I(ta.ema, close, length=8)
        self.ema_slow = self.I(ta.ema, close, length=21)
    
    def next(self):
        if not self.position:
            # Quick entry on fast EMA crossover and RSI recovery
            if (self.is_valid_signal(self.ema_fast, self.ema_slow, self.rsi_fast) and
                self.ema_fast[-1] > self.ema_slow[-1] and
                self.rsi_fast[-1] > 40 and self.rsi_fast[-1] < 60):
                self.buy()
        else:
            # Quick exit on reversal
            if (self.is_valid_signal(self.ema_fast, self.ema_slow, self.rsi_fast) and
                (self.ema_fast[-1] < self.ema_slow[-1] or 
                 self.rsi_fast[-1] < 35 or self.rsi_fast[-1] > 70)):
                self.sell()

# 3. YOUR CUSTOM STRATEGIES
class YourCustomMACDAS(BaseStrategy):
    """Your custom MACDAS strategy"""
    
    def init(self):
        close, high, low, volume = self.setup_common_indicators()
        
        # Your custom MACDAS indicator
        def get_macdas(close):
            macd_data = ta.macd(close, fast=12, slow=26, signal=9)
            return macd_data.iloc[:, 0] - macd_data.iloc[:, 1]
        
        def get_macdas_signal(close):
            macd_data = ta.macd(close, fast=12, slow=26, signal=9)
            macdas = macd_data.iloc[:, 0] - macd_data.iloc[:, 1]
            return macdas.ewm(span=9).mean()
        
        self.macdas = self.I(get_macdas, close)
        self.macdas_signal = self.I(get_macdas_signal, close)
        
        # Additional indicators
        self.mfi = self.I(ta.mfi, high, low, close, volume, length=14)
        
        def get_supertrend_direction(high, low, close):
            st_data = ta.supertrend(high, low, close, length=10, multiplier=3)
            return st_data.iloc[:, 1]
        
        self.supertrend_dir = self.I(get_supertrend_direction, high, low, close)
    
    def next(self):
        if not self.position:
            # Your custom entry logic
            if (self.is_valid_signal(self.macdas, self.macdas_signal, self.rsi, self.mfi, self.supertrend_dir) and
                self.macdas[-1] > self.macdas_signal[-1] and
                self.rsi[-1] < 40 and
                self.mfi[-1] < 30 and
                self.supertrend_dir[-1] == 1):
                self.buy()
        else:
            # Your custom exit logic
            if (self.is_valid_signal(self.macdas, self.macdas_signal, self.rsi, self.supertrend_dir) and
                (self.macdas[-1] < self.macdas_signal[-1] or
                 self.rsi[-1] > 70 or
                 self.supertrend_dir[-1] == -1)):
                self.sell()

# =============================================================================
# STRATEGY MANAGER AND TESTING FRAMEWORK
# =============================================================================

class StrategyManager:
    """Manage and organize multiple strategies"""
    
    def __init__(self):
        self.strategies = {
            # Trend Following
            'trend_following': TrendFollowingStrategy,
            
            # Momentum
            'momentum': MomentumStrategy,
            
            # Mean Reversion
            'mean_reversion': MeanReversionStrategy,
            
            # Multi-Signal
            'conservative': ConservativeStrategy,
            'aggressive': AggressiveStrategy,
            
            # Custom
            'macdas_custom': YourCustomMACDAS,
        }
        
        self.results = {}
    
    def list_strategies(self):
        """List all available strategies"""
        print("📋 AVAILABLE STRATEGIES:")
        print("=" * 40)
        for name, strategy_class in self.strategies.items():
            print(f"• {name}: {strategy_class.__doc__ or 'No description'}")
    
    def get_strategy(self, name):
        """Get strategy class by name"""
        if name not in self.strategies:
            raise ValueError(f"Strategy '{name}' not found. Available: {list(self.strategies.keys())}")
        return self.strategies[name]
    
    def add_custom_strategy(self, name, strategy_class):
        """Add a custom strategy"""
        self.strategies[name] = strategy_class
        print(f"✅ Added custom strategy: {name}")
    
    def run_single_strategy(self, strategy_name, symbol="AAPL", start_date="2022-01-01", end_date="2024-01-01"):
        """Run a single strategy"""
        strategy_class = self.get_strategy(strategy_name)
        
        # Get data
        data = self.prepare_data(symbol, start_date, end_date)
        
        # Run backtest
        bt = Backtest(data, strategy_class, cash=10000, commission=0.002)
        stats = bt.run()
        
        # Store results
        self.results[f"{strategy_name}_{symbol}"] = stats
        
        # Display results
        self.display_results(strategy_name, symbol, stats)
        
        return bt, stats
    
    def run_strategy_comparison(self, strategies, symbol="AAPL", start_date="2022-01-01", end_date="2024-01-01"):
        """Compare multiple strategies on the same symbol"""
        results = {}
        
        print(f"\n🔥 STRATEGY COMPARISON: {symbol}")
        print("=" * 60)
        
        for strategy_name in strategies:
            try:
                print(f"\n🚀 Testing {strategy_name}...")
                bt, stats = self.run_single_strategy(strategy_name, symbol, start_date, end_date)
                results[strategy_name] = stats
            except Exception as e:
                print(f"❌ Error with {strategy_name}: {e}")
        
        # Comparison table
        self.display_comparison(results, symbol)
        return results
    
    def run_multi_asset_test(self, strategy_name, symbols, start_date="2022-01-01", end_date="2024-01-01"):
        """Test one strategy across multiple assets"""
        results = {}
        
        print(f"\n🎯 MULTI-ASSET TEST: {strategy_name}")
        print("=" * 60)
        
        for symbol in symbols:
            try:
                print(f"\n📈 Testing {symbol}...")
                bt, stats = self.run_single_strategy(strategy_name, symbol, start_date, end_date)
                results[symbol] = stats
            except Exception as e:
                print(f"❌ Error with {symbol}: {e}")
        
        # Multi-asset comparison
        self.display_multi_asset_results(results, strategy_name)
        return results
    
    @staticmethod
    def prepare_data(symbol, start_date, end_date):
        """Prepare data for backtesting"""
        data = yf.download(symbol, start=start_date, end=end_date, progress=False)
        if hasattr(data.columns, 'levels'):
            data.columns = data.columns.droplevel(1)
        return data
    
    @staticmethod
    def display_results(strategy_name, symbol, stats):
        """Display individual strategy results"""
        print(f"\n📊 {strategy_name.upper()} RESULTS for {symbol}:")
        print("-" * 50)
        print(f"Return: {stats['Return [%]']:.2f}%")
        print(f"Buy & Hold: {stats['Buy & Hold Return [%]']:.2f}%")
        print(f"Sharpe Ratio: {stats['Sharpe Ratio']:.2f}")
        print(f"Max Drawdown: {stats['Max. Drawdown [%]']:.2f}%")
        print(f"Trades: {stats['# Trades']}")
        print(f"Win Rate: {stats['Win Rate [%]']:.1f}%")
    
    @staticmethod
    def display_comparison(results, symbol):
        """Display strategy comparison table"""
        if not results:
            return
        
        print(f"\n📈 STRATEGY COMPARISON SUMMARY: {symbol}")
        print("=" * 80)
        print(f"{'Strategy':<15} {'Return %':<10} {'Sharpe':<8} {'Max DD %':<10} {'Trades':<8} {'Win %':<8}")
        print("-" * 80)
        
        for strategy, stats in results.items():
            print(f"{strategy:<15} {stats['Return [%]']:<10.1f} {stats['Sharpe Ratio']:<8.2f} "
                  f"{stats['Max. Drawdown [%]']:<10.1f} {stats['# Trades']:<8} {stats['Win Rate [%]']:<8.1f}")
    
    @staticmethod
    def display_multi_asset_results(results, strategy_name):
        """Display multi-asset test results"""
        if not results:
            return
        
        print(f"\n🌍 MULTI-ASSET RESULTS: {strategy_name}")
        print("=" * 70)
        print(f"{'Symbol':<8} {'Return %':<10} {'Sharpe':<8} {'Max DD %':<10} {'Trades':<8} {'Win %':<8}")
        print("-" * 70)
        
        for symbol, stats in results.items():
            print(f"{symbol:<8} {stats['Return [%]']:<10.1f} {stats['Sharpe Ratio']:<8.2f} "
                  f"{stats['Max. Drawdown [%]']:<10.1f} {stats['# Trades']:<8} {stats['Win Rate [%]']:<8.1f}")

# =============================================================================
# USAGE EXAMPLES
# =============================================================================

def main():
    """Main function showing how to use the organized strategies"""
    
    # Create strategy manager
    manager = StrategyManager()
    
    # List available strategies
    manager.list_strategies()
    
    # Example 1: Run a single strategy
    print("\n" + "="*60)
    print("EXAMPLE 1: Single Strategy Test")
    print("="*60)
    bt, stats = manager.run_single_strategy('trend_following', 'AAPL')
    
    # Example 2: Compare multiple strategies
    print("\n" + "="*60)
    print("EXAMPLE 2: Strategy Comparison")
    print("="*60)
    strategies_to_compare = ['trend_following', 'momentum', 'conservative']
    comparison_results = manager.run_strategy_comparison(strategies_to_compare, 'AAPL')
    
    # Example 3: Test one strategy across multiple stocks
    print("\n" + "="*60)
    print("EXAMPLE 3: Multi-Asset Test")
    print("="*60)
    symbols = ['AAPL', 'MSFT', 'GOOGL']
    multi_asset_results = manager.run_multi_asset_test('macdas_custom', symbols)
    
    # Example 4: Add your own custom strategy
    print("\n" + "="*60)
    print("EXAMPLE 4: Adding Custom Strategy")
    print("="*60)
    
    class MyPersonalStrategy(BaseStrategy):
        """My personal trading strategy"""
        def init(self):
            close, high, low, volume = self.setup_common_indicators()
            self.ema = self.I(ta.ema, close, length=12)
        
        def next(self):
            if not self.position and self.data.Close[-1] > self.ema[-1]:
                self.buy()
            elif self.position and self.data.Close[-1] < self.ema[-1]:
                self.sell()
    
    manager.add_custom_strategy('my_personal', MyPersonalStrategy)
    bt, stats = manager.run_single_strategy('my_personal', 'AAPL')

if __name__ == "__main__":
    main()