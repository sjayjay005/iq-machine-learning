"""
Unit tests for the trading strategies.
"""
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np

from iqoption_startup.strategies.bollinger_bands import (
    calculate_bollinger_bands, analyze_bollinger_bands
)

class TestBollingerBandsStrategy(unittest.TestCase):
    """Test cases for the Bollinger Bands strategy."""

    def test_calculate_bollinger_bands(self):
        """Test calculation of Bollinger Bands."""
        # Create sample candle data
        candles = [
            {'open': 1.0, 'close': 1.1, 'high': 1.2, 'low': 0.9, 'volume': 100, 'from': 1000},
            {'open': 1.1, 'close': 1.2, 'high': 1.3, 'low': 1.0, 'volume': 200, 'from': 2000},
            {'open': 1.2, 'close': 1.3, 'high': 1.4, 'low': 1.1, 'volume': 300, 'from': 3000},
            {'open': 1.3, 'close': 1.4, 'high': 1.5, 'low': 1.2, 'volume': 400, 'from': 4000},
            {'open': 1.4, 'close': 1.5, 'high': 1.6, 'low': 1.3, 'volume': 500, 'from': 5000},
            {'open': 1.5, 'close': 1.6, 'high': 1.7, 'low': 1.4, 'volume': 600, 'from': 6000},
            {'open': 1.6, 'close': 1.7, 'high': 1.8, 'low': 1.5, 'volume': 700, 'from': 7000},
        ]

        # Calculate Bollinger Bands
        df = calculate_bollinger_bands(candles, period=5, std_dev=2)

        # Assertions
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIn('middle_band', df.columns)
        self.assertIn('upper_band', df.columns)
        self.assertIn('lower_band', df.columns)
        
        # Check that the middle band is the moving average of close prices
        # For the last row, it should be the average of the last 5 close prices
        expected_ma = sum([1.3, 1.4, 1.5, 1.6, 1.7]) / 5
        self.assertAlmostEqual(df['middle_band'].iloc[-1], expected_ma, places=4)
        
        # Check that the bands are calculated correctly
        # The standard deviation of the last 5 close prices
        std_dev_value = np.std([1.3, 1.4, 1.5, 1.6, 1.7])
        expected_upper = expected_ma + (std_dev_value * 2)
        expected_lower = expected_ma - (std_dev_value * 2)
        
        self.assertAlmostEqual(df['upper_band'].iloc[-1], expected_upper, places=4)
        self.assertAlmostEqual(df['lower_band'].iloc[-1], expected_lower, places=4)

    def test_analyze_bollinger_bands_uptrend_green_candle(self):
        """Test analysis of Bollinger Bands with uptrend and green candle."""
        # Create a DataFrame with an uptrend and a green candle that doesn't touch the middle band
        df = pd.DataFrame({
            'open': [1.0, 1.1, 1.2, 1.3, 1.4, 1.5],
            'close': [1.1, 1.2, 1.3, 1.4, 1.5, 1.6],
            'middle_band': [1.0, 1.1, 1.2, 1.3, 1.4, 1.5],
            'upper_band': [1.2, 1.3, 1.4, 1.5, 1.6, 1.7],
            'lower_band': [0.8, 0.9, 1.0, 1.1, 1.2, 1.3]
        })
        
        # The last candle is green (close > open) and doesn't touch the middle band
        # (middle_band is not between open and close)
        signal = analyze_bollinger_bands(df)
        
        # Should generate a "call" signal
        self.assertEqual(signal, "call")

    def test_analyze_bollinger_bands_downtrend_red_candle(self):
        """Test analysis of Bollinger Bands with downtrend and red candle."""
        # Create a DataFrame with a downtrend and a red candle that doesn't touch the middle band
        df = pd.DataFrame({
            'open': [1.6, 1.5, 1.4, 1.3, 1.2, 1.1],
            'close': [1.5, 1.4, 1.3, 1.2, 1.1, 1.0],
            'middle_band': [1.6, 1.5, 1.4, 1.3, 1.2, 1.1],
            'upper_band': [1.8, 1.7, 1.6, 1.5, 1.4, 1.3],
            'lower_band': [1.4, 1.3, 1.2, 1.1, 1.0, 0.9]
        })
        
        # The last candle is red (close < open) and doesn't touch the middle band
        signal = analyze_bollinger_bands(df)
        
        # Should generate a "put" signal
        self.assertEqual(signal, "put")

    def test_analyze_bollinger_bands_no_signal(self):
        """Test analysis of Bollinger Bands with no clear signal."""
        # Create a DataFrame with no clear trend
        df = pd.DataFrame({
            'open': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            'close': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            'middle_band': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            'upper_band': [1.2, 1.2, 1.2, 1.2, 1.2, 1.2],
            'lower_band': [0.8, 0.8, 0.8, 0.8, 0.8, 0.8]
        })
        
        # No trend, all candles touch the middle band
        signal = analyze_bollinger_bands(df)
        
        # Should generate no signal
        self.assertEqual(signal, "none")

class TestMartingaleStrategy(unittest.TestCase):
    """Test cases for the Martingale strategy."""

    def test_betting_table_structure(self):
        """Test the structure of the betting table."""
        from iqoption_startup.strategies.martingale import BETTING_TABLE
        
        # Check that the betting table has the expected structure
        self.assertIn("$1", BETTING_TABLE)
        self.assertIn("$5", BETTING_TABLE)
        self.assertIn("$50", BETTING_TABLE)
        self.assertIn("$300", BETTING_TABLE)
        
        # Check that each level has the expected keys
        for level in BETTING_TABLE.values():
            self.assertIn("level_1_bet", level)
            self.assertIn("level_2_bet", level)
            self.assertIn("level_1_profit", level)
            self.assertIn("level_2_profit_after_covering_loss", level)

if __name__ == '__main__':
    unittest.main()
