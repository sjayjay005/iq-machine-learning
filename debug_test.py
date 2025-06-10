import logging
import sys
import time
import signal
from iqoptionapi.stable_api import IQ_Option

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('debug_test.log')
    ]
)

logger = logging.getLogger(__name__)

# Set a timeout for operations
class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("Operation timed out")

# Register the signal function handler
signal.signal(signal.SIGALRM, timeout_handler)

def test_connection():
    logger.info("Testing connection to IQ Option API...")

    # Replace with your IQ Option credentials or use dummy ones for testing
    email = "test@example.com"
    password = "test_password"

    # Connect to IQ Option with timeout
    logger.info("Connecting to IQ Option...")
    iq = IQ_Option(email, password)

    try:
        # Set 30 second timeout for connection
        signal.alarm(30)
        logger.info("Starting connection with 30 second timeout...")
        connection_status, reason = iq.connect()
        # Cancel the timeout if connection completes
        signal.alarm(0)

        if connection_status:
            logger.info("Connection successful!")
        else:
            logger.warning(f"Connection failed: {reason}")

        # Test websocket connection status
        logger.info(f"Websocket connected: {iq.check_connect()}")

    except TimeoutError:
        logger.error("Connection attempt timed out after 30 seconds")
        connection_status = False
        reason = "Timeout"
    except Exception as e:
        logger.error(f"Unexpected error during connection: {e}")
        logger.exception("Exception details:")
        connection_status = False
        reason = str(e)

    return iq, connection_status

def test_api_functions(iq):
    logger.info("Testing API functions...")

    # Test getting server time
    logger.info("Testing server time...")
    try:
        signal.alarm(10)  # 10 second timeout
        server_time = iq.get_server_timestamp()
        signal.alarm(0)  # Cancel the timeout
        logger.info(f"Server time: {server_time}")
    except TimeoutError:
        logger.error("Getting server time timed out after 10 seconds")
    except Exception as e:
        logger.error(f"Error getting server time: {e}")

    # Test getting profile info (should work even with invalid credentials)
    logger.info("Testing profile info...")
    try:
        signal.alarm(10)  # 10 second timeout
        iq.get_profile_ansyc()
        signal.alarm(0)  # Cancel the timeout
        logger.info("Profile info request sent")
    except TimeoutError:
        logger.error("Getting profile info timed out after 10 seconds")
    except Exception as e:
        logger.error(f"Error getting profile info: {e}")

    # Test getting balance info
    logger.info("Testing balance info...")
    try:
        signal.alarm(10)  # 10 second timeout
        balance_type = "PRACTICE"  # or "REAL"
        iq.change_balance(balance_type)
        balance = iq.get_balance()
        signal.alarm(0)  # Cancel the timeout
        logger.info(f"{balance_type} balance: {balance}")
    except TimeoutError:
        logger.error("Getting balance info timed out after 10 seconds")
    except Exception as e:
        logger.error(f"Error getting balance: {e}")

    # Test getting available assets
    logger.info("Testing available assets...")
    try:
        signal.alarm(20)  # 20 second timeout for assets (might take longer)
        assets = iq.get_all_open_time()
        signal.alarm(0)  # Cancel the timeout

        binary_assets = assets["binary"]
        turbo_assets = assets["turbo"]
        digital_assets = assets["digital"]

        logger.info(f"Binary assets count: {len([a for a in binary_assets if binary_assets[a]['open']])}")
        logger.info(f"Turbo assets count: {len([a for a in turbo_assets if turbo_assets[a]['open']])}")
        logger.info(f"Digital assets count: {len([a for a in digital_assets if digital_assets[a]['open']])}")
    except TimeoutError:
        logger.error("Getting available assets timed out after 20 seconds")
    except Exception as e:
        logger.error(f"Error getting assets: {e}")

def main():
    logger.info("Starting debug test...")

    try:
        # Set an overall timeout for the entire script
        signal.alarm(120)  # 2 minute overall timeout

        try:
            iq, connection_status = test_connection()

            # Even if connection fails due to invalid credentials, we can still test some API functions
            test_api_functions(iq)

            # Wait a bit to ensure all websocket messages are processed
            logger.info("Waiting for 3 seconds to process any pending messages...")
            time.sleep(3)

        except TimeoutError:
            logger.error("Overall script execution timed out after 120 seconds")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            logger.exception("Exception details:")
        finally:
            # Cancel the overall timeout
            signal.alarm(0)

            # Try to close any open connections
            try:
                logger.info("Attempting to close any open connections...")
                # If we have a websocket connection, try to close it properly
                if 'iq' in locals() and hasattr(iq, 'close'):
                    iq.close()
            except Exception as e:
                logger.error(f"Error closing connections: {e}")

    except Exception as e:
        logger.error(f"Critical error in main function: {e}")
        logger.exception("Exception details:")

    logger.info("Debug test completed.")

if __name__ == "__main__":
    main()
