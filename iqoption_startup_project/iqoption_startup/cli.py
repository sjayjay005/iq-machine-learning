"""
IQ Option API Command Line Interface

This module provides a command-line interface for the IQ Option API.
"""
import os
import logging
from dotenv import load_dotenv

from .api.connection import connect_to_iqoption
from .utils.helpers import (
    get_balance, display_available_assets, place_binary_option_trade, 
    check_trade_result
)
from .strategies.martingale import run_strategy as run_martingale_strategy
from .strategies.bollinger_bands import run_strategy as run_bollinger_bands_strategy

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("iqoption_api.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Main function to demonstrate IQ Option API usage"""
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

    # Get trading settings from environment variables
    balance_type = os.getenv("DEFAULT_BALANCE_TYPE", "PRACTICE")
    default_asset = os.getenv("DEFAULT_ASSET", "EURUSD")
    default_amount = float(os.getenv("DEFAULT_AMOUNT", "1"))
    default_duration = int(os.getenv("DEFAULT_DURATION", "1"))

    # Get balance
    balance = get_balance(api, balance_type)

    # Display available assets
    display_available_assets(api)

    # Simple menu
    print("\n=== IQ Option Trading Demo ===")
    print(f"1. Place a CALL trade on {default_asset}")
    print(f"2. Place a PUT trade on {default_asset}")
    print("3. Run Martingale Strategy Simulator")
    print("4. Run Bollinger Bands Strategy")
    print("5. Exit")

    choice = input("\nEnter your choice (1-5): ")

    if choice == "1":
        success, order_id = place_binary_option_trade(
            api, default_asset, default_amount, "call", default_duration
        )
        if success:
            print(f"Waiting {default_duration} minute(s) for trade to expire...")
            import time
            time.sleep(default_duration * 60)
            result, profit = check_trade_result(api, order_id)
            print(f"Trade result: {result.upper()} (Profit/Loss: {profit})")

    elif choice == "2":
        success, order_id = place_binary_option_trade(
            api, default_asset, default_amount, "put", default_duration
        )
        if success:
            print(f"Waiting {default_duration} minute(s) for trade to expire...")
            import time
            time.sleep(default_duration * 60)
            result, profit = check_trade_result(api, order_id)
            print(f"Trade result: {result.upper()} (Profit/Loss: {profit})")

    elif choice == "3":
        # Run the martingale strategy simulator
        run_martingale_strategy()

    elif choice == "4":
        # Run the Bollinger Bands strategy
        run_bollinger_bands_strategy()

    elif choice == "5":
        print("Exiting...")

    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
