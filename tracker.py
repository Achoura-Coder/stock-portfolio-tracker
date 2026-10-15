from datetime import datetime

from data import CURRENCY_RATES, DIVERSIFICATION_LIMIT, STOCK_PRICES


def log_transaction(transactions, kind, symbol, quantity, price):
    """Add a BUY or SELL line to the transaction history."""
    transactions.append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "type": kind,
        "symbol": symbol,
        "quantity": quantity,
        "price": price,
    })


def add_stock(portfolio, transactions, symbol, quantity, buy_price):
    """Buy shares. If we already own the stock, the buy price becomes an average."""
    if symbol not in STOCK_PRICES:
        raise ValueError(f"Unknown stock: {symbol}")
    if quantity <= 0 or buy_price <= 0:
        raise ValueError("Quantity and price must be greater than 0.")

    if symbol in portfolio:
        old = portfolio[symbol]
        new_quantity = old["quantity"] + quantity
        total_paid = old["quantity"] * old["buy_price"] + quantity * buy_price
        portfolio[symbol] = {
            "quantity": new_quantity,
            "buy_price": total_paid / new_quantity,
        }
    else:
        portfolio[symbol] = {"quantity": quantity, "buy_price": buy_price}

    log_transaction(transactions, "BUY", symbol, quantity, buy_price)


def sell_stock(portfolio, transactions, symbol, quantity):
    """Sell shares at the current price. Return the value of the sale."""
    if symbol not in portfolio:
        raise ValueError(f"You don't own {symbol}.")
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")

    owned = portfolio[symbol]["quantity"]
    if quantity > owned:
        raise ValueError(f"You only own {owned} shares of {symbol}.")

    price = STOCK_PRICES[symbol]
    portfolio[symbol]["quantity"] -= quantity
    if portfolio[symbol]["quantity"] == 0:
        del portfolio[symbol]

    log_transaction(transactions, "SELL", symbol, quantity, price)
    return quantity * price


def position_value(symbol, position):
    """Current value of one position."""
    return STOCK_PRICES[symbol] * position["quantity"]


def total_value(portfolio):
    """Current value of the whole portfolio."""
    return sum(position_value(name, pos) for name, pos in portfolio.items())


def total_cost(portfolio):
    """Total amount paid for the whole portfolio."""
    return sum(pos["quantity"] * pos["buy_price"] for pos in portfolio.values())


def profit_percent(symbol, position):
    """Profit or loss of one position, in percent."""
    buy = position["buy_price"]
    return (STOCK_PRICES[symbol] - buy) / buy * 100


def get_profit(portfolio):
    """Return (profit, profit in percent) for the whole portfolio."""
    cost = total_cost(portfolio)
    profit = total_value(portfolio) - cost
    percent = profit / cost * 100 if cost else 0
    return profit, percent


def get_allocation(portfolio):
    """Return {symbol: percent of the portfolio value}."""
    total = total_value(portfolio)
    if total == 0:
        return {}
    return {
        name: position_value(name, pos) / total * 100
        for name, pos in portfolio.items()
    }


def make_bar(percent, width=20):
    """Draw a bar like ████░░░░ for a percentage."""
    filled = round(percent / 100 * width)
    return "█" * filled + "░" * (width - filled)


def get_warnings(portfolio):
    """Warn if one stock is too big compared to the rest."""
    warnings = []
    for name, percent in get_allocation(portfolio).items():
        if percent > DIVERSIFICATION_LIMIT:
            warnings.append(
                f"Warning: {name} is {percent:.0f}% of your portfolio "
                f"(limit is {DIVERSIFICATION_LIMIT}%)."
            )
    return warnings


def get_highlights(portfolio):
    """Return (best performing stock, largest position), or None if empty."""
    if not portfolio:
        return None
    best = max(portfolio, key=lambda s: profit_percent(s, portfolio[s]))
    largest = max(portfolio, key=lambda s: position_value(s, portfolio[s]))
    return best, largest


def simulate(portfolio, change_percent, symbol=None):
    """Total value if prices change by x%. symbol=None means all stocks."""
    total = 0
    for name, position in portfolio.items():
        price = STOCK_PRICES[name]
        if symbol is None or name == symbol:
            price = price * (1 + change_percent / 100)
        total += price * position["quantity"]
    return total


def convert(amount_usd, currency):
    """Convert a USD amount to another currency."""
    return amount_usd * CURRENCY_RATES[currency]


def build_report(portfolio):
    """Return the portfolio as a text table."""
    header = (
        f"{'Stock':<7}{'Qty':>5}{'Buy':>10}{'Now':>10}"
        f"{'Value':>12}{'Profit':>11}{'%':>9}"
    )
    lines = [header, "-" * len(header)]

    for name, position in portfolio.items():
        qty = position["quantity"]
        buy = position["buy_price"]
        now = STOCK_PRICES[name]
        value = qty * now
        profit = value - qty * buy
        percent = profit_percent(name, position)
        lines.append(
            f"{name:<7}{qty:>5}{buy:>10.2f}{now:>10.2f}"
            f"{value:>12.2f}{profit:>+11.2f}{percent:>+8.1f}%"
        )

    profit, percent = get_profit(portfolio)
    lines.append("-" * len(header))
    lines.append(f"Total invested: ${total_cost(portfolio):,.2f}")
    lines.append(f"Total value:    ${total_value(portfolio):,.2f}")
    lines.append(f"Profit/loss:    {profit:+,.2f} USD ({percent:+.2f}%)")
    return "\n".join(lines)