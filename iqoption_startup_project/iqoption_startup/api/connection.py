"""
IQ Option API Connection Module

This module provides functions for connecting to the IQ Option API.
"""
import time
import logging
from iqoptionapi.stable_api import IQ_Option

logger = logging.getLogger(__name__)

def connect_to_iqoption(email, password, max_retries=1):
    """
    Connect to IQ Option API with retry mechanism

    Args:
        email (str): IQ Option account email
        password (str): IQ Option account password
        max_retries (int): Maximum number of connection attempts (default: 1)

    Returns:
        IQ_Option: API instance if connection successful, None otherwise
    """
    logger.info("Connecting to IQ Option...")
    api = IQ_Option(email, password)

    # Ensure max_retries is an integer
    if max_retries is None:
        max_retries = 1

    retry_delay = 5  # seconds

    for attempt in range(max_retries):
        try:
            connection_status, reason = api.connect()

            if connection_status:
                logger.info("Connection successful")

                # Verify the connection is fully established
                if api.check_connect():
                    logger.info("Connection verified")

                    # Initialize the API by getting profile data
                    try:
                        profile = api.get_profile_ansyc()
                        if profile:
                            logger.info(f"Connected as: {profile.get('name', 'Unknown')}")
                        else:
                            logger.warning("Profile data is empty")

                        # Ensure we have the balance information
                        try:
                            balances = api.get_balances()
                            if balances:
                                logger.info(f"Account balances retrieved successfully")
                            else:
                                logger.warning("Could not retrieve account balances")
                        except TimeoutError as te:
                            logger.warning(f"Timeout getting balances: {str(te)}")
                        except Exception as be:
                            logger.warning(f"Error getting balances: {str(be)}")
                    except TimeoutError as te:
                        logger.warning(f"Timeout getting profile data: {str(te)}")
                    except Exception as e:
                        logger.warning(f"Could not retrieve profile data: {str(e)}")

                    return api
                else:
                    logger.warning("Connection status check failed")
            else:
                logger.error(f"Connection attempt {attempt+1}/{max_retries} failed: {reason}")

                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
        except Exception as e:
            logger.error(f"Exception during connection attempt {attempt+1}/{max_retries}: {str(e)}")

            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff

    logger.error(f"Failed to connect after {max_retries} attempts")
    return None
