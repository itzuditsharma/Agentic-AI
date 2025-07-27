class Account:
    def __init__(self, user_id: str, initial_deposit: float) -> None:
        self.user_id = user_id
        self.balance = initial_deposit
        self.holdings = {}
        self.transactions = []
        self.initial_deposit = initial_deposit

    def deposit(self, amount: float) -> None:
        self.balance += amount
        self.transactions.append(("deposit", amount))

    def withdraw(self, amount: float) -> bool:
        if amount <= self.balance:
            self.balance -= amount
            self.transactions.append(("withdraw", amount))
            return True
        return False

    def buy_shares(self, symbol: str, quantity: int) -> bool:
        price = get_share_price(symbol)
        cost = price * quantity
        if cost <= self.balance:
            self.balance -= cost
            self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
            self.transactions.append(("buy", symbol, quantity, price))
            return True
        return False

    def sell_shares(self, symbol: str, quantity: int) -> bool:
        if symbol in self.holdings and self.holdings[symbol] >= quantity:
            price = get_share_price(symbol)
            revenue = price * quantity
            self.balance += revenue
            self.holdings[symbol] -= quantity
            self.transactions.append(("sell", symbol, quantity, price))
            return True
        return False

    def calculate_portfolio_value(self) -> float:
        return sum(get_share_price(symbol) * quantity for symbol, quantity in self.holdings.items())

    def calculate_profit_loss(self) -> float:
        return (self.calculate_portfolio_value() + self.balance) - self.initial_deposit

    def get_holdings(self) -> dict:
        return dict(self.holdings)

    def get_transaction_history(self) -> list:
        return list(self.transactions)

    def get_profit_loss_at_time(self, timestamp: float) -> float:
        # Assume this function is not implemented due to lack of historical data context
        raise NotImplementedError("Historical data functionality not implemented.")


# Function to get the current price of a share
def get_share_price(symbol: str) -> float:
    prices = {
        "AAPL": 150.0,
        "TSLA": 700.0,
        "GOOGL": 2800.0
    }
    return prices.get(symbol, 0.0)


# Example Usage:
if __name__ == "__main__":
    account = Account(user_id="user123", initial_deposit=10000)
    account.deposit(500)
    account.withdraw(200)
    account.buy_shares("AAPL", 10)
    account.sell_shares("AAPL", 5)
    
    print("Balance:", account.balance)
    print("Portfolio Value:", account.calculate_portfolio_value())
    print("Profit/Loss:", account.calculate_profit_loss())
    print("Holdings:", account.get_holdings())
    print("Transaction History:", account.get_transaction_history())