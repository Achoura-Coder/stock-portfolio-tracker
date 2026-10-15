import unittest

from data import CURRENCY_RATES, STOCK_PRICES
from tracker import (
    add_stock, convert, get_allocation, get_profit, get_warnings,
    make_bar, sell_stock, simulate, total_value,
)


class TestTracker(unittest.TestCase):
    def setUp(self):
        self.portfolio = {}
        self.transactions = []

    def buy(self, symbol, quantity, price):
        add_stock(self.portfolio, self.transactions, symbol, quantity, price)

    def test_add_stock(self):
        self.buy("AAPL", 10, 150)
        self.assertEqual(self.portfolio["AAPL"]["quantity"], 10)
        self.assertEqual(len(self.transactions), 1)

    def test_buy_twice_averages_price(self):
        self.buy("AAPL", 10, 100)
        self.buy("AAPL", 10, 200)
        self.assertEqual(self.portfolio["AAPL"]["quantity"], 20)
        self.assertEqual(self.portfolio["AAPL"]["buy_price"], 150)

    def test_unknown_stock(self):
        with self.assertRaises(ValueError):
            self.buy("XYZ", 1, 10)

    def test_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.buy("AAPL", 0, 100)

    def test_sell_part(self):
        self.buy("AAPL", 10, 100)
        sell_stock(self.portfolio, self.transactions, "AAPL", 4)
        self.assertEqual(self.portfolio["AAPL"]["quantity"], 6)

    def test_sell_all_removes_stock(self):
        self.buy("AAPL", 10, 100)
        sell_stock(self.portfolio, self.transactions, "AAPL", 10)
        self.assertNotIn("AAPL", self.portfolio)

    def test_sell_too_many(self):
        self.buy("AAPL", 5, 100)
        with self.assertRaises(ValueError):
            sell_stock(self.portfolio, self.transactions, "AAPL", 6)

    def test_total_value(self):
        self.buy("AAPL", 10, 100)
        self.assertEqual(total_value(self.portfolio), 10 * STOCK_PRICES["AAPL"])

    def test_profit(self):
        self.buy("AAPL", 10, 100)
        expected = 10 * (STOCK_PRICES["AAPL"] - 100)
        profit, percent = get_profit(self.portfolio)
        self.assertAlmostEqual(profit, expected)
        self.assertAlmostEqual(percent, expected / 1000 * 100)

    def test_allocation_sums_to_100(self):
        self.buy("AAPL", 10, 100)
        self.buy("TSLA", 5, 100)
        self.assertAlmostEqual(sum(get_allocation(self.portfolio).values()), 100)

    def test_simulate_all(self):
        self.buy("AAPL", 10, 100)
        expected = total_value(self.portfolio) * 1.1
        self.assertAlmostEqual(simulate(self.portfolio, 10), expected)

    def test_simulate_one_stock(self):
        self.buy("AAPL", 10, 100)
        self.buy("TSLA", 5, 100)
        expected = 10 * STOCK_PRICES["AAPL"] * 1.1 + 5 * STOCK_PRICES["TSLA"]
        self.assertAlmostEqual(simulate(self.portfolio, 10, "AAPL"), expected)

    def test_warning_when_one_stock_only(self):
        self.buy("AAPL", 10, 100)
        self.assertEqual(len(get_warnings(self.portfolio)), 1)

    def test_no_warning_when_balanced(self):
        # same total value for both stocks: exactly 50% each
        self.buy("AAPL", STOCK_PRICES["TSLA"], 100)
        self.buy("TSLA", STOCK_PRICES["AAPL"], 100)
        self.assertEqual(get_warnings(self.portfolio), [])

    def test_convert(self):
        self.assertEqual(convert(100, "XOF"), 100 * CURRENCY_RATES["XOF"])

    def test_make_bar(self):
        self.assertEqual(make_bar(50, 10), "█████░░░░░")


if __name__ == "__main__":
    unittest.main()