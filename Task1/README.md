# Task 1: Moving Average Strategy

## Overview

This task implements a Moving Average trading strategy for analyzing Bitcoin (BTC-USD) price data. It fetches historical Bitcoin data, calculates moving averages, and generates trading signals based on the strategy.

## Features

- **Historical Data Fetching**: Retrieves BTC-USD price data from Yahoo Finance
- **Moving Average Calculation**: Computes short-term and long-term moving averages
- **Trading Strategy**: Generates buy/sell signals based on moving average crossovers
- **Data Analysis**: Analyzes stock performance over the specified period

## Prerequisites

Make sure you have completed the main project setup:

1. ✅ Created virtual environment (`venv`)
2. ✅ Activated the virtual environment
3. ✅ Installed dependencies from `requirements.txt`

If not, go back to the main [README.md](../README.md) and follow the setup instructions.

## How to Run

From the **main project directory** (`pythonProjectAssignment`), run:

```powershell
python -m Task1.main
```

### What It Does

The script will:
1. Fetch BTC-USD price data from January 1, 2024 to October 20, 2025
2. Calculate moving averages with a window of 500 periods
3. Generate trading signals and analysis
4. Display results in the console

## Configuration

Edit the parameters in `Task1/main.py` to customize the strategy:

```python
strategy = MovingAverageStrategy(
    "BTC-USD",           # Asset ticker
    "2024-01-01",        # Start date
    "2025-10-20",        # End date
    500                  # Moving average window
)
```

### Parameters:
- **ticker**: Asset symbol (e.g., "BTC-USD", "ETH-USD", "AAPL")
- **start_date**: Analysis start date (YYYY-MM-DD format)
- **end_date**: Analysis end date (YYYY-MM-DD format)
- **window**: Moving average period in days

## Project Structure

```
Task1/
├── main.py                           # Entry point
├── core/
│   ├── data_fetcher.py              # Yahoo Finance data retrieval
│   ├── GoldenOpportunity.py         # Strategy implementation
│   ├── indicator.py                 # Technical indicators
│   ├── profile.py                   # Stock profile data
│   └── __init__.py
├── strategies/
│   ├── MovingAverageSrategy.py      # Moving average strategy class
│   └── __init__.py
└── __pycache__/
```

## Technical Details

### Moving Average Strategy

The strategy uses:
- **Input Data**: Daily BTC-USD price data
- **Calculation**: SMA (Simple Moving Average) with configurable window
- **Signal Generation**: Buy/Sell signals from crossovers

### Dependencies Used

- `yfinance` - Fetches historical stock data
- `pandas` - Data manipulation and analysis
- `numpy` - Numerical computations
- `requests` - HTTP requests (if needed)

## Troubleshooting

### "ModuleNotFoundError: No module named 'Task1'"
- Ensure you're running the command from the **main project directory**
- Verify the virtual environment is activated (look for `(assignemnt)` in prompt)

### "No data available" or "Invalid ticker"
- Check the ticker symbol is correct
- Verify internet connection (yfinance needs to fetch from Yahoo Finance)
- Ensure date range is valid and contains trading days

### Import Errors
- Reinstall dependencies: `pip install --force-reinstall -r requirements.txt`
- Check that `core/` and `strategies/` directories have `__init__.py` files

## Notes

- Warnings are suppressed in the main script for cleaner output
- The strategy uses 500-day moving average by default for longer-term trends
- Data is fetched from Yahoo Finance (free and no API key required)

## Related Documentation

- [Main README](../README.md) - Project overview and setup
- [Task 2 README](../Task2/README.md) - Alternative task documentation
