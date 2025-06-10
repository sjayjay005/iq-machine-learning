#!/usr/bin/env python3
"""
Example script to demonstrate how to get historical candle data from IQ Option API
and perform a simple moving average analysis.
"""
import os
import time
import logging
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
from iqoption_startup.api.connection import connect_to_iqoption

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_candles(api, asset, timeframe, count, end_time=None):
    """
    Get historical candles for an asset

    Args:
        api (IQ_Option): API instance
        asset (str): Asset name (e.g., "EURUSD")
        timeframe (int): Candle timeframe in seconds (e.g., 60 for 1 minute)
        count (int): Number of candles to get
        end_time (datetime, optional): End time for the candles. Defaults to now.

    Returns:
        list: List of candle data
    """
    if end_time is None:
        end_time = datetime.now()

    # Convert to timestamp in milliseconds
    end_timestamp = int(end_time.timestamp())

    logger.info(f"Getting {count} candles for {asset} with {timeframe}s timeframe")
    candles = api.get_candles(asset, timeframe, count, end_timestamp)

    logger.info(f"Retrieved {len(candles)} candles")
    return candles

def calculate_moving_averages(candles, short_period=5, long_period=20):
    """
    Calculate simple moving averages from candle data

    Args:
        candles (list): List of candle data
        short_period (int): Short period for MA
        long_period (int): Long period for MA

    Returns:
        tuple: (DataFrame with candles and MAs, last short MA, last long MA)
    """
    # Convert candles to DataFrame
    df = pd.DataFrame(candles)

    # Rename columns for clarity
    df = df.rename(columns={
        'from': 'timestamp',
        'open': 'open',
        'close': 'close',
        'high': 'high',
        'low': 'low',
        'volume': 'volume'
    })

    # Convert timestamp to datetime
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')

    # Calculate moving averages
    df[f'SMA_{short_period}'] = df['close'].rolling(window=short_period).mean()
    df[f'SMA_{long_period}'] = df['close'].rolling(window=long_period).mean()

    # Get last values
    last_short_ma = df[f'SMA_{short_period}'].iloc[-1]
    last_long_ma = df[f'SMA_{long_period}'].iloc[-1]

    return df, last_short_ma, last_long_ma

def analyze_trend(df, short_period=5, long_period=20):
    """
    Analyze trend based on moving average crossovers

    Args:
        df (DataFrame): DataFrame with candle data and MAs
        short_period (int): Short period for MA
        long_period (int): Long period for MA

    Returns:
        str: Trend analysis
    """
    # Get the last few values of the MAs
    short_ma = df[f'SMA_{short_period}'].dropna()
    long_ma = df[f'SMA_{long_period}'].dropna()

    # Check if we have enough data
    if len(short_ma) < 2 or len(long_ma) < 2:
        return "Not enough data for trend analysis"

    # Check for crossover
    current_diff = short_ma.iloc[-1] - long_ma.iloc[-1]
    previous_diff = short_ma.iloc[-2] - long_ma.iloc[-2]

    if current_diff > 0 and previous_diff <= 0:
        return "BULLISH CROSSOVER - Short MA crossed above Long MA"
    elif current_diff < 0 and previous_diff >= 0:
        return "BEARISH CROSSOVER - Short MA crossed below Long MA"
    elif current_diff > 0:
        return "BULLISH TREND - Short MA above Long MA"
    else:
        return "BEARISH TREND - Short MA below Long MA"

def main():
    """Main function to demonstrate getting historical data"""
    # Load environment variables
    load_dotenv()

    # Get credentials from environment variables
    email = os.getenv("IQ_OPTION_EMAIL")
    password = os.getenv("IQ_OPTION_PASSWORD")

    if not email or not password:
        logger.error("Email or password not set in .env file")
        print("Please create a .env file with your credentials (see .env.example)")
        return

    # Connect to IQ Option with retry mechanism (3 attempts)
    api = connect_to_iqoption(email, password, max_retries=3)
    if not api:
        return

    # Set to practice account
    api.change_balance("PRACTICE")

    # Parameters
    asset = "EURUSD"
    timeframe = 60  # 1 minute candles
    candle_count = 100
    short_period = 5
    long_period = 20

    # Get candles
    candles = get_candles(api, asset, timeframe, candle_count)

    # Calculate moving averages
    df, last_short_ma, last_long_ma = calculate_moving_averages(
        candles, short_period, long_period
    )

    # Print the last 5 candles with MAs
    print("\n=== Last 5 Candles with Moving Averages ===")
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    print(df[['datetime', 'open', 'high', 'low', 'close', f'SMA_{short_period}', f'SMA_{long_period}']].tail())

    # Analyze trend
    trend = analyze_trend(df, short_period, long_period)
    print(f"\nTrend Analysis: {trend}")

    # Simple trading signal
    print("\n=== Trading Signal Based on Moving Averages ===")
    if last_short_ma > last_long_ma:
        print(f"SIGNAL: BUY (Short MA {last_short_ma:.5f} > Long MA {last_long_ma:.5f})")
    else:
        print(f"SIGNAL: SELL (Short MA {last_short_ma:.5f} < Long MA {last_long_ma:.5f})")

if __name__ == "__main__":
    main()
