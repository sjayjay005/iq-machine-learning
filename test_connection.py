import logging
import sys
import os
from iqoptionapi.stable_api import IQ_Option
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

# Get credentials from environment variables
email = os.getenv('IQ_OPTION_EMAIL')
password = os.getenv('IQ_OPTION_PASSWORD')

if not email or not password:
    print("Please set IQ_OPTION_EMAIL and IQ_OPTION_PASSWORD environment variables")
    sys.exit(1)

# Connect to IQ Option
print("Connecting to IQ Option...")
iq = IQ_Option(email, password)
connection_status, reason = iq.connect()

if connection_status:
    print("Connection successful!")
else:
    print(f"Connection failed: {reason}")

print("Test completed.")
