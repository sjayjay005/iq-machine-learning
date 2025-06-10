# Bollinger Bands Trading Strategy Documentation

## Overview

The Bollinger Bands trading strategy implemented in this project is designed for trading on the IQ Option platform. This strategy uses Bollinger Bands, a popular technical analysis tool, to identify potential trading opportunities in various financial markets.

## Strategy Parameters

- **Timeframe**: 2-minute candles
- **Trade Duration**: 2-minute expiry
- **Maximum Trades**: 15 trades per day
- **Bollinger Bands Settings**: 
  - Period: 7 (number of candles used for calculation)
  - Standard Deviation: 3 (multiplier for the standard deviation)
- **Target Payout**: 70% or above
- **Markets**: Focuses on OTC (Over-The-Counter) assets for more consistent trading opportunities

## How the Strategy Works

### Signal Generation Logic

The Bollinger Bands strategy generates trading signals based on the following rules:

1. **Trend Detection**: The strategy first determines if there's an uptrend or downtrend by calculating the slope of the middle band (simple moving average) over the last 5 candles.

2. **Candle Analysis**: The strategy then looks for the first candle that doesn't touch the middle band.

3. **Signal Generation**:
   - If the non-touching candle is green (close > open), a "CALL" signal is generated
   - If the non-touching candle is red (close < open), a "PUT" signal is generated
   - If no clear signal is detected, no trade is placed

4. **Trade Continuation**: Once a trading direction (CALL or PUT) is established, the strategy continues trading in that direction until a new signal is generated.

### Asset Selection Process

The strategy automatically selects the best assets to trade using the following process:

1. **OTC Asset Discovery**: The strategy identifies all available OTC assets across different markets (binary, turbo, digital).

2. **Asset Validation**: Each asset is validated by checking if it's open for trading and retrieving a test candle.

3. **Payout Filtering**: Assets with payouts below the minimum threshold (70%) are filtered out.

4. **Ranking**: The remaining assets are ranked by payout percentage, with the highest payout assets prioritized.

## Implementation Details

### Key Components

The strategy implementation consists of several key components:

1. **Bollinger Bands Calculation**: The `calculate_bollinger_bands()` function calculates the Bollinger Bands from candle data, handling different API response formats.

2. **Signal Analysis**: The `analyze_bollinger_bands()` function analyzes the Bollinger Bands to generate trading signals.

3. **Asset Selection**: The `get_all_otc_assets()` and `get_top_otc_assets()` functions identify and rank the best assets to trade.

4. **Trade Execution**: The `place_multiple_binary_option_trades()` function places trades concurrently using threads.

5. **Result Monitoring**: The `check_multiple_trade_results()` function monitors the results of multiple trades.

### Error Handling

The strategy includes robust error handling mechanisms:

- **Connection Verification**: Periodically verifies the API connection is still active
- **Retry Logic**: Implements retry mechanisms with exponential backoff for API calls
- **Fallback Mechanisms**: Provides fallbacks for different API response formats
- **Exception Handling**: Catches and logs exceptions at multiple levels

## Usage Guide

### Running the Strategy

You can run the Bollinger Bands strategy in two ways:

1. **From the Command Line**:
   ```bash
   iqoption-trade
   ```
   Then select option 4 from the menu.

2. **From Python Code**:
   ```python
   from iqoption_startup.strategies.bollinger_bands import run_strategy
   
   # Run the strategy
   run_strategy()
   ```

### User Interaction

When running the strategy, you'll be presented with several options:

1. **Asset Selection**:
   - Use the top asset only
   - Select a specific asset from the list
   - Monitor all top 10 assets

2. **Strategy Monitoring**:
   - The strategy will display real-time information about candles, signals, and trades
   - Trade results will be shown after each trade expires
   - A summary will be displayed at the end of the session

### Configuration

You can configure the strategy by modifying the following environment variables in your `.env` file:

```
IQ_OPTION_EMAIL=your_email@example.com
IQ_OPTION_PASSWORD=your_password
DEFAULT_BALANCE_TYPE=PRACTICE  # PRACTICE or REAL
DEFAULT_AMOUNT=1  # Trade amount
```

## Performance Considerations

### Optimal Market Conditions

The Bollinger Bands strategy tends to perform best under the following conditions:

- **Trending Markets**: The strategy works well in markets with clear trends
- **Moderate Volatility**: Too little volatility may not generate signals, while too much can lead to false signals
- **OTC Markets**: OTC assets often have more consistent behavior than regular markets

### Risk Management

The strategy implements several risk management features:

- **Maximum Trade Limit**: Limits the number of trades to 15 per day
- **Payout Filtering**: Only trades assets with payouts above 70%
- **Balance Monitoring**: Tracks and displays balance changes after each trade

## Customization Options

You can customize the strategy by modifying the following parameters in the code:

- **Bollinger Bands Period**: Change the number of candles used for calculation (default: 7)
- **Standard Deviation Multiplier**: Adjust the width of the bands (default: 3)
- **Timeframe**: Modify the candle timeframe (default: 120 seconds)
- **Trade Duration**: Change the expiry time for trades (default: 2 minutes)
- **Maximum Trades**: Adjust the maximum number of trades per day (default: 15)

## Troubleshooting

### Common Issues

1. **No Trading Signals**:
   - Check if the selected assets are open for trading
   - Verify that the market has sufficient volatility
   - Consider adjusting the Bollinger Bands parameters

2. **Connection Problems**:
   - Ensure your internet connection is stable
   - Check if the IQ Option API is accessible
   - Verify your account credentials

3. **Low Payouts**:
   - Try different assets or markets
   - Trade during peak market hours for better payouts
   - Consider adjusting the minimum payout threshold

## Disclaimer

This trading strategy is provided for educational purposes only. Trading financial instruments involves risk, and past performance is not indicative of future results. Never trade with money you cannot afford to lose.

Always test the strategy thoroughly in a demo account before using it with real funds.