"""
IQ Option API Utility Functions

This module provides common utility functions for working with the IQ Option API.

The module includes functions for trading with different instrument types (binary, digital, blitz/turbo)
with automatic switching between instrument types if one is not available for trading.

Key functions:
- place_binary_option_trade: Place a binary option trade (prefers binary options)
- place_digital_option_trade: Place a digital option trade (prefers digital options)
- place_blitz_option_trade: Place a blitz/turbo option trade (prefers turbo options)
- switch_to_available_instrument: Helper function to find an available instrument
"""
import os
import time
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def check_asset_open(api, asset, market_type=None):
    """
    Check if an asset is open for trading

    Args:
        api (IQ_Option): API instance
        asset (str): Asset name (e.g., "EURUSD")
        market_type (str, optional): Specific market type to check (e.g., "binary", "turbo", "digital")

    Returns:
        bool: True if asset is open, False otherwise
    """
    try:
        all_assets = api.get_all_open_time()

        # If market_type is specified, only check that market
        if market_type:
            if market_type in all_assets and asset in all_assets[market_type]:
                is_open = all_assets[market_type][asset]["open"]
                logger.info(f"Asset {asset} in {market_type} market is {'open' if is_open else 'closed'}")
                return is_open
            else:
                logger.warning(f"Asset {asset} not found in {market_type} market")
                return False

        # Otherwise check all markets
        for market in all_assets:
            if asset in all_assets[market]:
                is_open = all_assets[market][asset]["open"]
                logger.info(f"Asset {asset} in {market} market is {'open' if is_open else 'closed'}")
                return is_open

        logger.warning(f"Asset {asset} not found in any market")
        return False
    except Exception as e:
        logger.error(f"Error checking if asset {asset} is open: {str(e)}")
        # Assume the asset is open if we can't determine its status
        # This allows the strategy to attempt to trade even if we can't check asset status
        logger.warning(f"Assuming asset {asset} is open due to error checking status")
        return True

def switch_to_available_instrument(api, asset, preferred_instruments=None):
    """
    Check if an asset is available in preferred instrument types and switch to another if not

    Args:
        api (IQ_Option): API instance
        asset (str): Asset name (e.g., "EURUSD")
        preferred_instruments (list, optional): List of preferred instrument types in order of preference
                                               (e.g., ["binary", "turbo", "digital"])
                                               Defaults to ["binary", "turbo", "digital"]

    Returns:
        tuple: (asset_name, instrument_type) - The asset name and instrument type to use
    """
    if preferred_instruments is None:
        preferred_instruments = ["binary", "turbo", "digital"]

    try:
        all_assets = api.get_all_open_time()

        # Check if the asset is available in any of the preferred instruments
        for instrument in preferred_instruments:
            # Check regular version
            if instrument in all_assets and asset in all_assets[instrument]:
                if all_assets[instrument][asset]["open"]:
                    logger.info(f"Asset {asset} is available in {instrument} market")
                    return asset, instrument

            # Check OTC version
            otc_asset = f"{asset}-OTC"
            if instrument in all_assets and otc_asset in all_assets[instrument]:
                if all_assets[instrument][otc_asset]["open"]:
                    logger.info(f"Switching to OTC version: {otc_asset} in {instrument} market")
                    return otc_asset, instrument

        # If we get here, try to find any open asset in the preferred instruments
        for instrument in preferred_instruments:
            if instrument in all_assets:
                for available_asset in all_assets[instrument]:
                    if all_assets[instrument][available_asset]["open"]:
                        logger.info(f"Switching to available asset: {available_asset} in {instrument} market")
                        return available_asset, instrument

        # If we get here, no suitable asset was found
        logger.warning(f"No suitable asset found in any of the preferred instruments: {preferred_instruments}")
        return asset, preferred_instruments[0]  # Return the original asset and first preferred instrument
    except Exception as e:
        logger.error(f"Error finding available instrument for asset {asset}: {str(e)}")
        # Return the original asset and first preferred instrument as fallback
        logger.warning(f"Using original asset {asset} with {preferred_instruments[0]} due to error checking availability")
        return asset, preferred_instruments[0]

def get_balance(api, balance_type="PRACTICE"):
    """
    Get account balance

    Args:
        api (IQ_Option): API instance
        balance_type (str): Balance type ("PRACTICE" or "REAL")

    Returns:
        float: Account balance
    """
    api.change_balance(balance_type)
    balance = api.get_balance()
    logger.info(f"{balance_type} balance: {balance}")
    return balance

def place_binary_option_trade(api, asset, amount, action, duration, preferred_instruments=None):
    """
    Place a binary option trade with retry mechanism and instrument switching

    Args:
        api (IQ_Option): API instance
        asset (str): Asset name (e.g., "EURUSD")
        amount (float): Trade amount
        action (str): Trade direction ("call" or "put")
        duration (int): Trade duration in minutes
        preferred_instruments (list, optional): List of preferred instrument types in order of preference
                                               (e.g., ["binary", "turbo", "digital"])
                                               Defaults to ["binary", "turbo", "digital"]

    Returns:
        tuple: (success status, order id)
    """
    logger.info(f"Placing {action} trade on {asset} for {amount} with {duration}m expiry")

    # Ensure balance_id is set by checking and changing balance if needed
    balance_type = os.getenv("DEFAULT_BALANCE_TYPE", "PRACTICE")
    current_balance_mode = api.get_balance_mode()

    if current_balance_mode != balance_type:
        logger.warning(f"Balance mode mismatch. Current: {current_balance_mode}, Expected: {balance_type}")
        logger.info(f"Changing balance mode to {balance_type}")
        api.change_balance(balance_type)
        time.sleep(1)  # Give the API time to process the change

    # Use the switch_to_available_instrument function to find an available instrument
    if preferred_instruments is None:
        preferred_instruments = ["binary", "turbo", "digital"]

    asset, instrument_type = switch_to_available_instrument(api, asset, preferred_instruments)
    logger.info(f"Using asset {asset} in {instrument_type} market")

    # Try to place the trade with retries
    max_retries = 3
    retry_delay = 2  # seconds

    for attempt in range(max_retries):
        try:
            # Use different methods based on the instrument type
            if instrument_type == "digital":
                success, order_id = api.buy_digital_spot(asset, amount, action, duration)
            else:  # binary or turbo
                success, order_id = api.buy(amount, asset, action, duration)

            if success:
                logger.info(f"Trade placed successfully on {instrument_type}. Order ID: {order_id}")
                return success, order_id
            else:
                error_msg = order_id if order_id else "Unknown error"
                logger.error(f"Trade failed: {error_msg}")

                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    logger.error(f"Failed to place trade after {max_retries} attempts")
                    return False, None
        except Exception as e:
            logger.error(f"Exception during trade placement: {str(e)}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                logger.error(f"Failed to place trade after {max_retries} attempts")
                return False, None

    return False, None

def place_blitz_option_trade(api, asset, amount, action, duration, preferred_instruments=None):
    """
    Place a blitz (turbo) option trade with retry mechanism and instrument switching

    Args:
        api (IQ_Option): API instance
        asset (str): Asset name (e.g., "EURUSD")
        amount (float): Trade amount
        action (str): Trade direction ("call" or "put")
        duration (int): Trade duration in minutes
        preferred_instruments (list, optional): List of preferred instrument types in order of preference
                                               (e.g., ["turbo", "binary", "digital"])
                                               Defaults to ["turbo", "binary", "digital"]

    Returns:
        tuple: (success status, order id)
    """
    logger.info(f"Placing blitz {action} trade on {asset} for {amount} with {duration}m expiry")

    # Ensure balance_id is set by checking and changing balance if needed
    balance_type = os.getenv("DEFAULT_BALANCE_TYPE", "PRACTICE")
    current_balance_mode = api.get_balance_mode()

    if current_balance_mode != balance_type:
        logger.warning(f"Balance mode mismatch. Current: {current_balance_mode}, Expected: {balance_type}")
        logger.info(f"Changing balance mode to {balance_type}")
        api.change_balance(balance_type)
        time.sleep(1)  # Give the API time to process the change

    # Use the switch_to_available_instrument function to find an available instrument
    if preferred_instruments is None:
        preferred_instruments = ["turbo", "binary", "digital"]

    asset, instrument_type = switch_to_available_instrument(api, asset, preferred_instruments)
    logger.info(f"Using asset {asset} in {instrument_type} market")

    # Try to place the trade with retries
    max_retries = 3
    retry_delay = 2  # seconds

    for attempt in range(max_retries):
        try:
            # Use different methods based on the instrument type
            if instrument_type == "digital":
                success, order_id = api.buy_digital_spot(asset, amount, action, duration)
            else:  # binary or turbo
                success, order_id = api.buy(amount, asset, action, duration)

            if success:
                logger.info(f"Trade placed successfully on {instrument_type}. Order ID: {order_id}")
                return success, order_id
            else:
                error_msg = order_id if order_id else "Unknown error"
                logger.error(f"Trade failed: {error_msg}")

                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    logger.error(f"Failed to place trade after {max_retries} attempts")
                    return False, None
        except Exception as e:
            logger.error(f"Exception during trade placement: {str(e)}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                logger.error(f"Failed to place trade after {max_retries} attempts")
                return False, None

    return False, None

def place_digital_option_trade(api, asset, amount, action, duration, preferred_instruments=None):
    """
    Place a digital option trade with retry mechanism and instrument switching

    Args:
        api (IQ_Option): API instance
        asset (str): Asset name (e.g., "EURUSD")
        amount (float): Trade amount
        action (str): Trade direction ("call" or "put")
        duration (int): Trade duration in minutes
        preferred_instruments (list, optional): List of preferred instrument types in order of preference
                                               (e.g., ["digital", "binary", "turbo"])
                                               Defaults to ["digital", "binary", "turbo"]

    Returns:
        tuple: (success status, order id)
    """
    logger.info(f"Placing digital {action} trade on {asset} for {amount} with {duration}m expiry")

    # Ensure balance_id is set by checking and changing balance if needed
    balance_type = os.getenv("DEFAULT_BALANCE_TYPE", "PRACTICE")
    current_balance_mode = api.get_balance_mode()

    if current_balance_mode != balance_type:
        logger.warning(f"Balance mode mismatch. Current: {current_balance_mode}, Expected: {balance_type}")
        logger.info(f"Changing balance mode to {balance_type}")
        api.change_balance(balance_type)
        time.sleep(1)  # Give the API time to process the change

    # Use the switch_to_available_instrument function to find an available instrument
    if preferred_instruments is None:
        preferred_instruments = ["digital", "binary", "turbo"]

    asset, instrument_type = switch_to_available_instrument(api, asset, preferred_instruments)
    logger.info(f"Using asset {asset} in {instrument_type} market")

    # Try to place the trade with retries
    max_retries = 3
    retry_delay = 2  # seconds

    for attempt in range(max_retries):
        try:
            # Use different methods based on the instrument type
            if instrument_type == "digital":
                success, order_id = api.buy_digital_spot(asset, amount, action, duration)
            else:  # binary or turbo
                success, order_id = api.buy(amount, asset, action, duration)

            if success:
                logger.info(f"Trade placed successfully on {instrument_type}. Order ID: {order_id}")
                return success, order_id
            else:
                error_msg = order_id if order_id else "Unknown error"
                logger.error(f"Trade failed: {error_msg}")

                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    logger.error(f"Failed to place trade after {max_retries} attempts")
                    return False, None
        except Exception as e:
            logger.error(f"Exception during trade placement: {str(e)}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                logger.error(f"Failed to place trade after {max_retries} attempts")
                return False, None

    return False, None

def check_trade_result(api, order_id):
    """
    Check the result of a trade

    Args:
        api (IQ_Option): API instance
        order_id (int): Order ID

    Returns:
        tuple: (result, profit/loss)
    """
    logger.info(f"Checking result for order {order_id}")

    # Wait for the order to be processed
    while api.get_async_order(order_id) is None:
        logger.info("Waiting for order to be processed...")
        time.sleep(1)

    result = api.check_win_v3(order_id)

    if result > 0:
        logger.info(f"Trade won! Profit: {result}")
        return "win", result
    elif result == 0:
        logger.info("Trade ended in a tie")
        return "tie", result
    else:
        logger.info(f"Trade lost. Loss: {result}")
        return "lose", result

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

def check_payout(api, asset, duration):
    """
    Check the payout percentage for an asset

    Args:
        api (IQ_Option): API instance
        asset (str): Asset name (e.g., "EURUSD")
        duration (int): Trade duration in minutes

    Returns:
        float: Payout percentage
    """
    logger.info(f"Checking payout for {asset} with {duration}m expiry")
    try:
        # Try to get digital profit (payout)
        payout = api.get_digital_current_profit(asset, duration)
        if payout is False:
            # Fallback to binary options profit
            all_profit = api.get_all_profit()
            if asset in all_profit:
                # all_profit is a nested dict with keys "binary" and "turbo"
                if "binary" in all_profit[asset]:
                    payout = all_profit[asset]["binary"] * 100  # Convert to percentage
                elif "turbo" in all_profit[asset]:
                    payout = all_profit[asset]["turbo"] * 100  # Convert to percentage
                else:
                    payout = 0
                    logger.warning(f"Could not get payout for {asset} (no binary or turbo data)")
            else:
                payout = 0
                logger.warning(f"Could not get payout for {asset}")
    except Exception as e:
        logger.error(f"Error getting payout: {str(e)}")
        # Fallback to binary options profit
        all_profit = api.get_all_profit()
        if asset in all_profit:
            # all_profit is a nested dict with keys "binary" and "turbo"
            if "binary" in all_profit[asset]:
                payout = all_profit[asset]["binary"] * 100  # Convert to percentage
            elif "turbo" in all_profit[asset]:
                payout = all_profit[asset]["turbo"] * 100  # Convert to percentage
            else:
                payout = 0
                logger.warning(f"Could not get payout for {asset} (no binary or turbo data)")
        else:
            payout = 0
            logger.warning(f"Could not get payout for {asset}")

    logger.info(f"Payout for {asset}: {payout}%")
    return payout

def display_available_assets(api):
    """
    Display available assets for trading

    Args:
        api (IQ_Option): API instance
    """
    logger.info("Fetching available assets...")
    try:
        all_assets = api.get_all_open_time()

        print("\n=== Available Assets ===")
        for market_type in all_assets:
            if not all_assets[market_type]:  # Skip empty markets
                continue

            print(f"\n{market_type.upper()} MARKET:")
            open_assets = []

            for asset in all_assets[market_type]:
                try:
                    if all_assets[market_type][asset]["open"]:
                        open_assets.append(asset)
                except (KeyError, TypeError):
                    continue

            # Print in columns
            if open_assets:
                open_assets.sort()
                for i in range(0, len(open_assets), 3):
                    row = open_assets[i:i + 3]
                    print("  ".join(f"{asset:<10}" for asset in row))
            else:
                print("  No open assets")
    except Exception as e:
        logger.error(f"Error fetching available assets: {str(e)}")
        print("Unable to fetch available assets at this time. Please try again later.")

        # Display default assets as fallback
        print("\n=== Default Assets (Fallback) ===")
        default_markets = {
            "FOREX": ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "USDCHF", "EURGBP"],
            "OTC": ["EURUSD-OTC", "EURGBP-OTC", "USDCHF-OTC", "EURJPY-OTC", "NZDUSD-OTC", "GBPUSD-OTC", "GBPCAD-OTC"]
        }

        for market_type, assets in default_markets.items():
            print(f"\n{market_type} MARKET:")
            assets.sort()
            for i in range(0, len(assets), 3):
                row = assets[i:i + 3]
                print("  ".join(f"{asset:<10}" for asset in row))
