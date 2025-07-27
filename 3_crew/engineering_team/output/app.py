import gradio as gr  
from accounts import Account, get_share_price  

account = Account(account_id='user123', initial_deposit=1000.0)  

def create_account(initial_deposit):  
    global account  
    account = Account(account_id='user123', initial_deposit=initial_deposit)  
    return "Account created successfully!"

def deposit(amount):  
    success = account.deposit_funds(amount)  
    return "Deposit successful!" if success else "Deposit failed!"

def withdraw(amount):  
    success = account.withdraw_funds(amount)  
    return "Withdrawal successful!" if success else "Withdrawal failed!"

def buy_shares(symbol, quantity):  
    success = account.buy_shares(symbol, quantity)  
    return "Shares bought!" if success else "Buy failed!"

def sell_shares(symbol, quantity):  
    success = account.sell_shares(symbol, quantity)  
    return "Shares sold!" if success else "Sell failed!"

def portfolio_value():  
    return f"Portfolio Value: {account.calculate_portfolio_value()}"

def profit_loss():  
    return f"Profit/Loss: {account.calculate_profit_loss()}"

def holdings():  
    return f"Holdings: {account.get_holdings()}"

def transactions():  
    return f"Transactions: {account.get_transactions()}"  

with gr.Blocks() as demo:  
    gr.Markdown("### Trading Simulation Platform")  
    with gr.Group():  
        gr.Button("Create Account").click(create_account, inputs=[gr.Number(label="Initial Deposit")], outputs="text")  
        gr.Button("Deposit Funds").click(deposit, inputs=[gr.Number(label="Amount to Deposit")], outputs="text")  
        gr.Button("Withdraw Funds").click(withdraw, inputs=[gr.Number(label="Amount to Withdraw")], outputs="text")  
        gr.Button("Buy Shares").click(buy_shares, inputs=[gr.Textbox(label="Symbol"), gr.Number(label="Quantity")], outputs="text")  
        gr.Button("Sell Shares").click(sell_shares, inputs=[gr.Textbox(label="Symbol"), gr.Number(label="Quantity")], outputs="text")  
        gr.Button("Portfolio Value").click(portfolio_value, outputs="text")  
        gr.Button("Profit/Loss").click(profit_loss, outputs="text")  
        gr.Button("View Holdings").click(holdings, outputs="text")  
        gr.Button("View Transactions").click(transactions, outputs="text")  

if __name__ == "__main__":  
    demo.launch()