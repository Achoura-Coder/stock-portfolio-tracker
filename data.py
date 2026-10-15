# Hardcoded stock prices (USD per share). Edit or add stocks here.
STOCK_PRICES = {
    "AAPL": 180,
    "TSLA": 250,
    "GOOGL": 140,
    "MSFT": 380,
    "AMZN": 170,
    "NVDA": 480,
    "META": 330,
}

# Fixed currency rates from 1 USD. Update them when you want.
CURRENCY_RATES = {
    "USD": 1,
    "EUR": 0.92,
    "XOF": 605,
}

# Warn when one stock is more than this % of the portfolio
DIVERSIFICATION_LIMIT = 50