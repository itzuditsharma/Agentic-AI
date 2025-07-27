import unittest
from accounts import Account, get_share_price

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account(user_id="user123", initial_deposit=10000)

    def test_initialization(self):
        self.assertEqual(self.account.user_id, "user123")
        self.assertEqual(self.account.balance, 10000)
        self.assertEqual(self.account.holdings, {})
        self.assertEqual(self.account.transactions, [])

    def test_deposit(self):
        self.account.deposit(1000)
        self.assertEqual(self.account.balance, 11000)
        self.assertIn(("deposit", 1000), self.account.transactions)

    def test_withdraw(self):
        result = self.account.withdraw(200)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 9800)
        self.assertIn(("withdraw", 200), self.account.transactions)

        result = self.account.withdraw(20000)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 9800)  # No change in balance

    def test_buy_shares(self):
        result = self.account.buy_shares("AAPL", 10)
        self.assertTrue(result)
        self.assertEqual(self.account.holdings["AAPL"], 10)
        self.assertEqual(self.account.balance, 8500)
        self.assertTrue(any(x[0] == "buy" and x[1] == "AAPL" for x in self.account.transactions))

        result = self.account.buy_shares("TSLA", 100)  # Cost exceeds current balance
        self.assertFalse(result)
        self.assertNotIn("TSLA", self.account.holdings)

    def test_sell_shares(self):
        self.account.buy_shares("AAPL", 10)
        result = self.account.sell_shares("AAPL", 5)
        self.assertTrue(result)
        self.assertEqual(self.account.holdings["AAPL"], 5)
        self.assertEqual(self.account.balance, 9250)
        self.assertTrue(any(x[0] == "sell" and x[1] == "AAPL" for x in self.account.transactions))

        result = self.account.sell_shares("AAPL", 10)  # Not enough shares to sell
        self.assertFalse(result)

    def test_calculate_portfolio_value(self):
        self.account.buy_shares("AAPL", 10)
        self.assertEqual(self.account.calculate_portfolio_value(), 1500)

    def test_calculate_profit_loss(self):
        self.assertEqual(self.account.calculate_profit_loss(), 0)  # No transactions yet
        self.account.buy_shares("AAPL", 10)
        self.assertEqual(self.account.calculate_profit_loss(), -1500)  # After purchase

    def test_get_holdings(self):
        self.account.buy_shares("AAPL", 10)
        self.assertEqual(self.account.get_holdings(), {"AAPL": 10})

    def test_get_transaction_history(self):
        self.account.deposit(1000)
        self.account.withdraw(500)
        self.assertEqual(self.account.get_transaction_history(), [("deposit", 1000), ("withdraw", 500)])

    def test_get_profit_loss_at_time_raises(self):
        self.assertRaises(NotImplementedError, self.account.get_profit_loss_at_time, 0)
        
if __name__ == '__main__':
    unittest.main()