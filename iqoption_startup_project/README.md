# IQ Option API Startup Project

A Python package for automated trading on the IQ Option platform, supporting binary options, digital options, forex, stocks, commodities, crypto, and ETFs.

## Features

- Proper Python package structure with clear separation of concerns
- Connect to IQ Option API with retry mechanism
- Check available assets and their status
- Get account balance
- Place binary option trades with error handling
- Monitor trade results
- Comprehensive logging
- Trading strategies:
  - Bollinger Bands strategy
  - Martingale strategy simulator
- Unit tests for core functionality

## Installation

### Prerequisites

- Python 3.6 or higher
- IQ Option account (you can create one at [IQ Option](https://iqoption.com/))
- Access to the phone number associated with your IQ Option account (for SMS verification)

### Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/iqoption_startup_project.git
   cd iqoption_startup_project
   ```

2. Install the package in development mode:
   ```bash
   pip install -e .
   ```

   This will install the package and its dependencies, including the iqoptionapi package directly from GitHub.

3. Create a `.env` file with your IQ Option credentials:
   ```bash
   cp .env.example .env
   ```

4. Edit the `.env` file and replace the placeholder values with your actual credentials:
   ```
   IQ_OPTION_EMAIL=your_actual_email@example.com
   IQ_OPTION_PASSWORD=your_actual_password

   # Trading Settings
   DEFAULT_BALANCE_TYPE=PRACTICE  # PRACTICE or REAL
   DEFAULT_ASSET=EURUSD
   DEFAULT_AMOUNT=1
   DEFAULT_DURATION=1  # in minutes
   ```

## Project Structure

The project follows a proper Python package structure:

```
iqoption_startup_project/
├── iqoption_startup/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── connection.py  # API connection functions
│   ├── strategies/
│   │   ├── __init__.py
│   │   ├── bollinger_bands.py
│   │   └── martingale.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py  # Common utility functions
│   └── cli.py  # Command-line interface
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   └── test_strategies.py
├── examples/
│   ├── get_historical_data.py
│   └── README.md
├── setup.py
├── requirements.txt
└── README.md
```

## Usage

### Command-Line Interface

After installation, you can use the command-line interface:

```bash
iqoption-trade
```

Alternatively, you can run the CLI module directly:

```bash
python -m iqoption_startup.cli
```

The CLI will:
1. Connect to your IQ Option account
2. Display your account balance
3. Show available assets for trading
4. Present a menu with the following options:
   - Place a CALL trade
   - Place a PUT trade
   - Run Martingale Strategy Simulator
   - Run Bollinger Bands Strategy
   - Exit

### Using as a Library

You can also use the package as a library in your own Python code:

```python
from iqoption_startup.api.connection import connect_to_iqoption
from iqoption_startup.utils.helpers import get_balance, place_binary_option_trade
from iqoption_startup.strategies.bollinger_bands import run_strategy as run_bollinger_bands

# Connect to IQ Option
api = connect_to_iqoption("your_email@example.com", "your_password")

# Get balance
balance = get_balance(api, "PRACTICE")
print(f"Balance: {balance}")

# Place a trade
success, order_id = place_binary_option_trade(api, "EURUSD", 1, "call", 1)
if success:
    print(f"Trade placed successfully. Order ID: {order_id}")

# Run Bollinger Bands strategy
run_bollinger_bands()
```

### Examples

Check out the `examples` directory for additional scripts demonstrating specific features:

- `examples/get_historical_data.py` - Shows how to retrieve historical candle data and perform simple moving average analysis

See the [Examples README](examples/README.md) for more details.

## Running Tests

To run the unit tests:

```bash
python -m unittest discover -s tests
```

## Advanced Usage

### Modifying Trading Parameters

You can modify the trading parameters in the `.env` file:

- `DEFAULT_BALANCE_TYPE`: Set to "PRACTICE" for demo account or "REAL" for real money
- `DEFAULT_ASSET`: The asset you want to trade (e.g., "EURUSD", "BTCUSD", etc.)
- `DEFAULT_AMOUNT`: The amount to trade
- `DEFAULT_DURATION`: The trade duration in minutes

### Adding More Strategies

You can add more trading strategies by creating new modules in the `iqoption_startup/strategies` directory. Each strategy should have a `run_strategy()` function that serves as the entry point.

### Extending Functionality

The project is designed to be easily extendable:

1. Add new utility functions in `iqoption_startup/utils/helpers.py`
2. Add new API functions in `iqoption_startup/api/connection.py`
3. Add new CLI options in `iqoption_startup/cli.py`

## Troubleshooting

### SMS Verification

IQ Option now requires SMS verification for account security. The API will automatically handle this by:

1. Detecting when SMS verification is required
2. Prompting you to enter the verification code sent to your phone
3. Submitting the code and continuing the connection process

Note: You may need to verify your account periodically as verification tokens expire.

### OpenSSL Compatibility Issues

If you encounter warnings about urllib3 and OpenSSL compatibility, this is handled automatically by pinning urllib3 to a compatible version in the requirements.txt file.

### Module Import Errors

If you encounter an error like `ModuleNotFoundError: No module named 'iqoptionapi.stable_api'`, it means the iqoptionapi package is not properly installed. To fix this:

1. Make sure you've installed the package with all dependencies:
   ```bash
   pip install -e .
   ```

2. If the error persists, you can install the iqoptionapi package directly from GitHub:
   ```bash
   pip install git+https://github.com/Lu-Yi-Hsun/iqoptionapi.git@master
   ```

3. Verify the installation by running:
   ```bash
   python -c "from iqoptionapi.stable_api import IQ_Option; print('Successfully imported')"
   ```

## Disclaimer

This project is for educational purposes only. Trading involves risk. Never trade with money you cannot afford to lose.

## Resources

- [IQ Option API Documentation](https://lu-yi-hsun.github.io/iqoptionapi/)
- [IQ Option Official Website](https://iqoption.com/)
