# IQ Option API

A Python wrapper for IQ Option API - trade binary options, digital options, forex, stocks, commodities, crypto, ETFs and more.

## Installation

### Method 1: Install from PyPI
```bash
pip install iqoptionapi
```

### Method 2: Install from source
```bash
git clone https://github.com/Lu-Yi-Hsun/iqoptionapi.git
cd iqoptionapi
pip install -r requirements.txt
pip install -e .
```

## Dependencies
- pylint
- requests
- websocket-client (>=1.6.4)

## Quick Start

```python
from iqoptionapi.stable_api import IQ_Option
import time
import logging

# Enable logging (optional)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

# Connect to IQ Option
api = IQ_Option("your_email", "your_password")
connection_status, reason = api.connect()

if connection_status:
    print("Connection successful")
else:
    print(f"Connection failed: {reason}")
    exit(1)

# Check if asset is open
print("Asset open status:", api.get_all_open_time()["forex"]["EURUSD"]["open"])

# Get balance
balance_type = "PRACTICE"  # or "REAL"
api.change_balance(balance_type)
print(f"Balance: {api.get_balance()}")

# Place a binary option trade
asset = "EURUSD"
amount = 1
action = "call"  # or "put"
duration = 1  # minute

success, order_id = api.buy(amount, asset, action, duration)
if success:
    print(f"Trade placed successfully. Order ID: {order_id}")
else:
    print("Trade failed")
```

## Documentation

### New Documentation
https://lu-yi-hsun.github.io/iqoptionapi/

### Old Documentation (Not Supported)
https://github.com/Lu-Yi-Hsun/iqoptionapi_private/blob/master/old_document.md

## Supported Features
- Binary Options
- Digital Options
- Forex
- Stocks
- Commodities
- Cryptocurrencies
- ETFs
- Asset information
- Real-time candles
- Historical data
- Technical indicators

## External Resources
- IQ Option Robot: https://npt-life.com/iq-option-robot
- IQ Option API (private version): https://npt-life.com/iq-option-api
- Olymptrade API: https://npt-life.com/olymptrade-api

# IQ Option API
The best IQ Option API for Python

## Table of Contents
- [Installation](#installation)
- [Features](#features)
- [Usage](#usage)
- [SMS Verification](#sms-verification)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## Installation
```bash
pip install -U git+https://github.com/Lu-Yi-Hsun/iqoptionapi.git
```

## Features
- Connect to IQ Option API
- Support for binary options, digital options, forex, stocks, commodities, crypto, and ETFs
- Real-time data
- Historical data
- Account management
- Trading operations
- SMS verification support
- Automatic switching to OTC markets when regular markets are closed (e.g., EURUSD to EURUSD-OTC)

## Usage
```python
from iqoptionapi.stable_api import IQ_Option
import time
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

# Connect to IQ Option
iqoption = IQ_Option("email", "password")
check, reason = iqoption.connect()

if check:
    print("Connection successful")

    # Get balance
    balance = iqoption.get_balance()
    print(f"Balance: {balance}")

    # Place a trade
    iqoption.buy(1, "EURUSD", "call", 1)
else:
    print(f"Connection failed: {reason}")
```

## SMS Verification
The API now supports SMS verification. When IQ Option requires verification, the API will:

1. Detect the verification requirement
2. Prompt you to enter the verification code sent to your phone
3. Submit the code and continue the connection process

Example of handling SMS verification:
```python
from iqoptionapi.stable_api import IQ_Option

# Connect to IQ Option
iqoption = IQ_Option("email", "password")
check, reason = iqoption.connect()

# If verification is required, you'll be prompted to enter the code
# The API will handle the verification process automatically

if check:
    print("Connection successful")
    # Continue with your trading operations
else:
    print(f"Connection failed: {reason}")
```

## Automatic OTC Market Switching
The API now automatically switches to OTC (Over-The-Counter) markets when regular markets are closed. This is particularly useful for trading EURUSD, which is no longer available in regular forex markets but is available as EURUSD-OTC in binary and turbo markets.

When you try to trade EURUSD and it's not available, the API will:
1. Check if EURUSD is available in the regular market
2. If not, check if EURUSD-OTC is available
3. Automatically switch to EURUSD-OTC if it's available

This feature works with the following methods:
- `buy()` - For binary options
- `buy_digital_spot()` - For digital options
- `buy_by_raw_expirations()` - For custom expiration times

Example:
```python
from iqoptionapi.stable_api import IQ_Option
import logging

# Enable logging to see when switching occurs
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

# Connect to IQ Option
iqoption = IQ_Option("email", "password")
check, reason = iqoption.connect()

if check:
    # Place a trade with EURUSD
    # If EURUSD is not available but EURUSD-OTC is, it will automatically switch
    success, order_id = iqoption.buy(1, "EURUSD", "call", 1)

    if success:
        print(f"Trade placed successfully. Order ID: {order_id}")
    else:
        print("Trade failed")
```

## Documentation
For more detailed documentation, please refer to the [docs](docs) directory.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
