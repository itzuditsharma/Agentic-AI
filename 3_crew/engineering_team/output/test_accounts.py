import unittest
from accounts import Account, get_share_price

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account(account_id='user123', initial_deposit=1000.0)

    def test_initial_balance(self):
        self.assertEqual(self.account.balance, 1000.0)

    def test_deposit_funds(self):
        self.assertTrue(self.account.deposit_funds(500.0))
        self.assertEqual(self.account.balance, 1500.0)

    def test_withdraw_funds(self):
        self.account.deposit_funds(500.0)
        self.assertTrue(self.account.withdraw_funds(200.0))
        self.assertEqual(self.account.balance, 1300.0)

    def test_withdraw_over_balance(self):
        self.assertFalse(self.account.withdraw_funds(2000.0))

    def test_buy_shares_success(self):
        self.assertTrue(self.account.buy_shares('AAPL', 5))
        self.assertEqual(self.account.balance, 1000.0 - (150.0 * 5))
        self.assertEqual(self.account.get_holdings().get('AAPL'), 5)

    def test_buy_shares_insufficient_funds(self):
        self.assertFalse(self.account.buy_shares('AAPL', 10))

    def test_sell_shares_success(self):
        self.account.buy_shares('AAPL', 5)
        self.assertTrue(self.account.sell_shares('AAPL', 2))
        self.assertEqual(self.account.get_holdings().get('AAPL'), 3)
        self.assertEqual(self.account.balance, 1000.0 - (150.0 * 5) + (150.0 * 2))

    def test_sell_shares_insufficient_quantity(self):
        self.assertFalse(self.account.sell_shares('AAPL', 10))

    def test_calculate_portfolio_value(self):
        self.account.deposit_funds(500.0)
        self.account.buy_shares('AAPL', 2)
        self.assertEqual(self.account.calculate_portfolio_value(), 1000.0 + 500.0 - (150.0 * 2))

    def test_calculate_profit_loss(self):
        self.account.deposit_funds(500.0)
        self.account.buy_shares('AAPL', 2)
        self.assertEqual(self.account.calculate_profit_loss(), (1000.0 + 500.0 - (150.0 * 2)) - 1000.0)

    def test_get_transactions(self):
        self.assertIn('Account created with initial deposit: 1000.0', self.account.get_transactions())

if __name__ == '__main__':
    unittest.main()