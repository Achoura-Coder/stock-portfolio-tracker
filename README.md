# Stock Portfolio Tracker

A terminal portfolio tracker built with Python.
CodeAlpha Python Programming Internship, Task 2.

## How to run
1. Install Python 3
2. Run `python main.py`
3. Choose an option in the menu

To run the tests: `python test_tracker.py`

## Features
- **Portfolio:** buy and sell stocks, with an average buy price when you buy the same stock twice
- **Analysis:** profit/loss, best performer, largest position, allocation bars
- **Warning:** alert when one stock is more than 50% of the portfolio
- **What-if simulator:** see the new value if prices go up or down by x%
- **Currencies:** portfolio value in USD, EUR and XOF (fixed rates)
- **History:** list of all buy and sell transactions
- **Save and export:** the portfolio is saved in JSON between sessions, and reports can be exported to TXT and CSV

## Example
```
--- Menu ---
1. Buy stock
...
Choose: 1
Stock symbol (or 'back'): AAPL
Quantity: 10
Buy price (Enter for market price $180):
Bought 10 x AAPL at $180.00.
```

## Project structure
- `data.py`: stock prices, currency rates and settings
- `tracker.py`: calculations (no input or print, so it is easy to test)
- `storage.py`: JSON save/load and TXT/CSV export
- `main.py`: menu and user interaction
- `test_tracker.py`: automatic tests with `unittest`

To add a stock or change a price, edit `data.py` only.

## Concepts used
Dictionaries (also nested), lists, functions, modules, input validation, exceptions,
file handling (`json`, `csv`), `datetime`, unit tests.

## Notes
- Prices are hardcoded, as the task asks. No internet connection is needed.
- Selling uses the current price from `data.py`.