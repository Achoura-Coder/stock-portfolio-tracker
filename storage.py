import csv
import json
from datetime import datetime

from data import STOCK_PRICES
from tracker import build_report, position_value, profit_percent

DATA_FILE = "portfolio_data.json"
TXT_FILE = "portfolio_report.txt"
CSV_FILE = "portfolio_report.csv"


def load_data():
    """Load the portfolio and the history. Start empty if there is no file."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}, []

    # ignore stocks that were removed from STOCK_PRICES
    portfolio = {
        name: pos for name, pos in data.get("portfolio", {}).items()
        if name in STOCK_PRICES
    }
    return portfolio, data.get("transactions", [])


def save_data(portfolio, transactions):
    """Save the portfolio and the history in a JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(
            {"portfolio": portfolio, "transactions": transactions},
            file,
            indent=2,
        )


def export_txt(portfolio, filename=TXT_FILE):
    """Write a readable report in a text file."""
    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"Stock Portfolio Report - {date}\n\n")
        file.write(build_report(portfolio) + "\n")


def export_csv(portfolio, filename=CSV_FILE):
    """Write the portfolio in a CSV file (opens in Excel)."""
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Symbol", "Quantity", "Buy price", "Current price",
            "Value", "Profit %",
        ])
        for name, position in portfolio.items():
            writer.writerow([
                name,
                position["quantity"],
                round(position["buy_price"], 2),
                STOCK_PRICES[name],
                round(position_value(name, position), 2),
                round(profit_percent(name, position), 2),
            ])