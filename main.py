from data import CURRENCY_RATES, STOCK_PRICES
from storage import CSV_FILE, TXT_FILE, export_csv, export_txt, load_data, save_data
from tracker import (
    add_stock, build_report, convert, get_allocation, get_highlights,
    get_profit, get_warnings, make_bar, position_value, profit_percent,
    sell_stock, simulate, total_value,
)


# --- input helpers ---
def ask_symbol(allowed):
    """Ask for a stock symbol. Return None if the user types 'back'."""
    while True:
        name = input("Stock symbol (or 'back'): ").upper().strip()
        if name == "BACK":
            return None
        if name in allowed:
            return name
        print(f"Choose one of: {', '.join(allowed)}")


def ask_quantity():
    """Ask for a whole number greater than 0."""
    while True:
        value = input("Quantity: ").strip()
        if value.isdigit() and int(value) > 0:
            return int(value)
        print("Enter a whole number greater than 0.")


def ask_float(prompt, default=None, allow_negative=False):
    """Ask for a number. Pressing Enter returns the default (if there is one)."""
    while True:
        value = input(prompt).strip()
        if value == "" and default is not None:
            return default
        try:
            number = float(value)
        except ValueError:
            print("Enter a number.")
            continue
        if number <= 0 and not allow_negative:
            print("The number must be greater than 0.")
            continue
        return number


def has_stocks(portfolio):
    """Tell the user when the portfolio is empty."""
    if not portfolio:
        print("Your portfolio is empty. Buy a stock first (option 1).")
        return False
    return True


# --- menu actions ---
def action_buy(portfolio, transactions):
    symbol = ask_symbol(STOCK_PRICES)
    if symbol is None:
        return
    quantity = ask_quantity()
    market = STOCK_PRICES[symbol]
    price = ask_float(f"Buy price (Enter for market price ${market}): ", default=market)
    try:
        add_stock(portfolio, transactions, symbol, quantity, price)
        print(f"Bought {quantity} x {symbol} at ${price:,.2f}.")
    except ValueError as error:
        print(error)


def action_sell(portfolio, transactions):
    if not has_stocks(portfolio):
        return
    owned = ", ".join(f"{n} ({p['quantity']})" for n, p in portfolio.items())
    print("You own:", owned)
    symbol = ask_symbol(portfolio)
    if symbol is None:
        return
    quantity = ask_quantity()
    try:
        sale = sell_stock(portfolio, transactions, symbol, quantity)
        print(f"Sold {quantity} x {symbol} for ${sale:,.2f}.")
    except ValueError as error:
        print(error)


def action_show(portfolio, transactions):
    if not has_stocks(portfolio):
        return
    print()
    print(build_report(portfolio))
    for warning in get_warnings(portfolio):
        print(warning)


def action_allocation(portfolio, transactions):
    if not has_stocks(portfolio):
        return
    allocation = get_allocation(portfolio)
    for name, percent in sorted(allocation.items(), key=lambda item: item[1], reverse=True):
        print(f"{name:<6} {make_bar(percent)} {percent:5.1f}%")
    for warning in get_warnings(portfolio):
        print(warning)


def action_profit(portfolio, transactions):
    if not has_stocks(portfolio):
        return
    profit, percent = get_profit(portfolio)
    print(f"Total profit/loss: {profit:+,.2f} USD ({percent:+.2f}%)")
    best, largest = get_highlights(portfolio)
    print(f"Best performer:   {best} ({profit_percent(best, portfolio[best]):+.1f}%)")
    print(f"Largest position: {largest} (${position_value(largest, portfolio[largest]):,.2f})")


def action_simulate(portfolio, transactions):
    if not has_stocks(portfolio):
        return
    choice = input("Stock symbol or ALL: ").upper().strip()
    if choice != "ALL" and choice not in portfolio:
        print("You don't own that stock.")
        return
    change = ask_float("Price change in % (example: 10 or -5): ", allow_negative=True)
    symbol = None if choice == "ALL" else choice

    before = total_value(portfolio)
    after = simulate(portfolio, change, symbol)
    print(f"Current value: ${before:,.2f}")
    print(f"After {change:+g}%: ${after:,.2f} ({after - before:+,.2f} USD)")


def action_currency(portfolio, transactions):
    if not has_stocks(portfolio):
        return
    total = total_value(portfolio)
    print("Portfolio value:")
    for currency in CURRENCY_RATES:
        print(f"  {currency}: {convert(total, currency):,.2f}")


def action_history(portfolio, transactions):
    if not transactions:
        print("No transactions yet.")
        return
    print("Last transactions:")
    for t in transactions[-15:]:
        print(
            f"  {t['date']}  {t['type']:<4} {t['symbol']:<6}"
            f"{t['quantity']:>4} @ ${t['price']:,.2f}"
        )


def action_export(portfolio, transactions):
    if not has_stocks(portfolio):
        return
    export_txt(portfolio)
    export_csv(portfolio)
    print(f"Saved {TXT_FILE} and {CSV_FILE}")


MENU = {
    "1": ("Buy stock", action_buy),
    "2": ("Sell stock", action_sell),
    "3": ("Show portfolio", action_show),
    "4": ("Allocation", action_allocation),
    "5": ("Profit / loss and highlights", action_profit),
    "6": ("What-if simulator", action_simulate),
    "7": ("Currency conversion", action_currency),
    "8": ("Transaction history", action_history),
    "9": ("Export report (TXT and CSV)", action_export),
}


# --- main program ---
def main():
    portfolio, transactions = load_data()
    print("Stock Portfolio Tracker")
    print("Available stocks:")
    for name, price in STOCK_PRICES.items():
        print(f"  {name}: ${price}")

    try:
        while True:
            print("\n--- Menu ---")
            for key, (label, _) in MENU.items():
                print(f"{key}. {label}")
            print("0. Save and quit")

            choice = input("Choose: ").strip()
            if choice == "0":
                break
            if choice in MENU:
                MENU[choice][1](portfolio, transactions)
                save_data(portfolio, transactions)
            else:
                print("Invalid choice.")
    except (KeyboardInterrupt, EOFError):
        print()

    save_data(portfolio, transactions)
    print("Goodbye!")


if __name__ == "__main__":
    main()