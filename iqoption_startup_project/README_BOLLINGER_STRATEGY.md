# Bollinger Bands Trading Strategy

This script implements an automated trading strategy for IQ Option based on Bollinger Bands.

## Strategy Overview

The strategy works as follows:

- **Timeframe**: 2-minute candles
- **Trade Duration**: 2 minutes
- **Maximum Trades**: 15 trades per day
- **Entry Conditions**:
  - **PUT Signal**: When price crosses above the upper Bollinger Band
  - **CALL Signal**: When price crosses below the lower Bollinger Band
- **Continuation Rule**: Once a position is entered (call or put), continue with the same direction for subsequent trades
- **Minimum Payout**: Targets assets with 70% payout or above
- **Bollinger Bands Settings**: Period = 7, Standard Deviation = 3
- **Asset Selection**: Always uses the top 10 assets with highest payout
- **Minimum Active Trades**: Ensures at least 4 trades are active at a time
- **Martingale Recovery**: Applies martingale strategy to losing trades to recoup losses
  - Increases trade amount after a loss by a factor of 2.5
  - Resets to base amount after a win
  - Maximum of 2 martingale levels

## Requirements

- Python 3.6+
- iqoptionapi
- pandas
- numpy
- python-dotenv

## Setup

1. Create a `.env` file in the project directory with your IQ Option credentials:

```
IQ_OPTION_EMAIL=your_email@example.com
IQ_OPTION_PASSWORD=your_password
DEFAULT_BALANCE_TYPE=PRACTICE  # Use PRACTICE or REAL
DEFAULT_ASSET=EURUSD  # Default asset to trade
DEFAULT_AMOUNT=1  # Default trade amount
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

Run the strategy with:

```bash
python bollinger_bands_strategy.py
```

## How It Works

1. The script connects to IQ Option API using your credentials
2. It identifies the top 10 OTC assets with the highest payout percentages
3. It verifies the payout percentages meet the minimum requirement (70%)
4. It continuously monitors the price action of all top 10 assets using Bollinger Bands:
   - When price crosses above the upper band, it places a PUT trade
   - When price crosses below the lower band, it places a CALL trade
   - Once a trade direction is established, it continues with the same direction
5. The script ensures at least 4 trades are active at any time (if possible)
   - If fewer than 4 assets have trading signals, it selects additional assets to meet the minimum
6. After each trade, it applies the martingale strategy:
   - If a trade wins, it resets the trade amount to the base amount
   - If a trade loses, it increases the trade amount by a factor of 2.5 for the next trade on that asset
   - It limits the martingale to a maximum of 2 levels
7. The script limits trading to a maximum of 15 trades per day
8. Results of each trade are logged and displayed, along with martingale levels for each asset

## Risk Warning

This is a demonstration strategy and should be used with caution:

- Always start with a PRACTICE account
- Past performance is not indicative of future results
- Trading involves risk of loss
- The strategy does not guarantee profits

## Customization

You can modify the following parameters in the script:

- `timeframe`: Candle timeframe in seconds (default: 120 for 2 minutes)
- `duration`: Trade duration in minutes (default: 2)
- `max_trades`: Maximum number of trades per day (default: 15)
- `bb_period`: Bollinger Bands period (default: 7)
- `bb_std_dev`: Bollinger Bands standard deviation multiplier (default: 3)
- `min_payout`: Minimum acceptable payout percentage (default: 70)
- `martingale_factor`: Multiplier for bet after a loss (default: 2.5)
- `max_martingale_level`: Maximum martingale level (default: 2)

## Logging

The script logs all activities to both the console and a log file (`iqoption_api.log`). This helps with debugging and analyzing the strategy's performance.
