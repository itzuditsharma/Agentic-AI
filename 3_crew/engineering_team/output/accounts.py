class Account:
    def __init__(self, account_id: str, initial_deposit: float) -> None:
        self.account_id = account_id
        self.balance = initial_deposit
        self.transactions = []
        self.holdings = {}
        self.initial_deposit = initial_deposit
        self.transactions.append(f'Account created with initial deposit: {initial_deposit}')

    def deposit_funds(self, amount: float) -> bool:
        if amount > 0:
            self.balance += amount
            self.transactions.append(f'Deposited: {amount}')
            return True
        return False

    def withdraw_funds(self, amount: float) -> bool:
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.transactions.append(f'Withdrew: {amount}')
            return True
        return False

    def buy_shares(self, symbol: str, quantity: int) -> bool:
        share_price = get_share_price(symbol)
        total_cost = share_price * quantity
        if quantity > 0 and total_cost <= self.balance:
            self.balance -= total_cost
            if symbol in self.holdings:
                self.holdings[symbol] += quantity
            else:
                self.holdings[symbol] = quantity
            self.transactions.append(f'Bought {quantity} shares of {symbol} at {share_price} each')
            return True
        return False

    def sell_shares(self, symbol: str, quantity: int) -> bool:
        if symbol in self.holdings and 0 < quantity <= self.holdings[symbol]:
            share_price = get_share_price(symbol)
            total_revenue = share_price * quantity
            self.balance += total_revenue
            self.holdings[symbol] -= quantity
            if self.holdings[symbol] == 0:
                del self.holdings[symbol]
            self.transactions.append(f'Sold {quantity} shares of {symbol} at {share_price} each')
            return True
        return False

    def calculate_portfolio_value(self) -> float:
        total_value = self.balance
        for symbol, quantity in self.holdings.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def calculate_profit_loss(self) -> float:
        return self.calculate_portfolio_value() - self.initial_deposit

    def get_holdings(self) -> dict:
        return self.holdings

    def get_transactions(self) -> list:
        return self.transactions


def get_share_price(symbol: str) -> float:
    prices = {'AAPL': 150.0, 'TSLA': 700.0, 'GOOGL': 2800.0}
    return prices.get(symbol, 0.0)

# Example usage in a testing context
if __name__ == '__main__':
    account = Account(account_id='user123', initial_deposit=1000.0)
    account.deposit_funds(500.0)
    account.withdraw_funds(200.0)
    account.buy_shares('AAPL', 5)
    account.sell_shares('AAPL', 2)
    portfolio_value = account.calculate_portfolio_value()
    profit_loss = account.calculate_profit_loss()
    holdings = account.get_holdings()
    transactions = account.get_transactions()
    print("Portfolio Value:", portfolio_value)
    print("Profit/Loss:", profit_loss)
    print("Holdings:", holdings)
    print("Transactions:", transactions)
