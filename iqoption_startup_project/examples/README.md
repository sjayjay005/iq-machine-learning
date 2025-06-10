# IQ Option API Examples

This directory contains example scripts that demonstrate various features of the IQ Option API.

## Available Examples

### 1. Historical Data Analysis (`get_historical_data.py`)

This example demonstrates how to:
- Retrieve historical candle data from IQ Option
- Convert the data to a pandas DataFrame
- Calculate simple moving averages (SMA)
- Analyze trends based on moving average crossovers
- Generate trading signals

#### Requirements
- pandas
- numpy

#### Usage
```bash
python get_historical_data.py
```

#### Example Output
```
2023-10-15 15:45:23 - __main__ - INFO - Connecting to IQ Option...
2023-10-15 15:45:25 - __main__ - INFO - Connection successful
2023-10-15 15:45:25 - __main__ - INFO - Getting 100 candles for EURUSD with 60s timeframe
2023-10-15 15:45:26 - __main__ - INFO - Retrieved 100 candles

=== Last 5 Candles with Moving Averages ===
                  datetime     open     high      low    close  SMA_5  SMA_20
95 2023-10-15 15:40:00  1.05321  1.05325  1.05318  1.05322  1.0532  1.0531
96 2023-10-15 15:41:00  1.05322  1.05326  1.05319  1.05324  1.0532  1.0531
97 2023-10-15 15:42:00  1.05324  1.05328  1.05321  1.05326  1.0532  1.0531
98 2023-10-15 15:43:00  1.05326  1.05330  1.05323  1.05328  1.0533  1.0531
99 2023-10-15 15:44:00  1.05328  1.05332  1.05325  1.05330  1.0533  1.0531

Trend Analysis: BULLISH TREND - Short MA above Long MA

=== Trading Signal Based on Moving Averages ===
SIGNAL: BUY (Short MA 1.05326 > Long MA 1.05312)
```

## Adding Your Own Examples

Feel free to add your own examples to this directory. When creating a new example:

1. Create a new Python file with a descriptive name
2. Add proper documentation and comments
3. Update this README.md to include your example

## Best Practices

- Always use the PRACTICE account for testing
- Include proper error handling
- Use environment variables for credentials
- Add logging for better debugging