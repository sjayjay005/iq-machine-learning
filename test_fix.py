from iqoptionapi.stable_api import IQ_Option
import time
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

# Create an instance of IQ_Option
api = IQ_Option("email", "password")

# Connect to initialize the api attribute
api.connect()

# Try to get all open time
try:
    all_assets = api.get_all_open_time()
    print("Success! All assets:", all_assets)
except KeyError as e:
    print(f"KeyError: {e}")
except Exception as e:
    print(f"Error: {e}")
