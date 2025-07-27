import gradio as gr
from accounts import Account, get_share_price

def create_account(user_id, initial_deposit):
    global account
    account = Account(user_id, initial_deposit)
    return f"Account created for {user_id} with deposit ${initial_deposit}"

def deposit(amount):
    account.deposit(amount)
    return f"Deposited ${amount}. New balance: ${account.balance}"

def withdraw(amount):
    if account.withdraw(amount):
        return f"Withdrew ${amount}. New balance: ${account.balance}"
    else:
        return f"Failed to withdraw ${amount}. Insufficient balance."

def buy_shares(symbol, quantity):
    if account.buy_shares(symbol, quantity):
        return f"Bought {quantity} shares of {symbol}."
    else:
        return f"Failed to buy shares. Insufficient funds."

def sell_shares(symbol, quantity):
    if account.sell_shares(symbol, quantity):
        return f"Sold {quantity} shares of {symbol}."
    else:
        return f"Failed to sell shares. Insufficient holdings."

def get_portfolio():
    return f"Balance: ${account.balance}, Portfolio Value: ${account.calculate_portfolio_value()}, Profit/Loss: ${account.calculate_profit_loss()}"

def get_holdings():
    return account.get_holdings()

def get_transactions():
    return account.get_transaction_history()

with gr.Blocks() as demo:
    with gr.Row():
        user_id = gr.Textbox(label="User ID")
        initial_deposit = gr.Number(label="Initial Deposit")
        create_btn = gr.Button("Create Account")
        create_btn.click(create_account, inputs=[user_id, initial_deposit], outputs=[])

    with gr.Row():
        deposit_amount = gr.Number(label="Deposit Amount")
        deposit_btn = gr.Button("Deposit")
        deposit_btn.click(deposit, inputs=deposit_amount, outputs=[])

    with gr.Row():
        withdraw_amount = gr.Number(label="Withdraw Amount")
        withdraw_btn = gr.Button("Withdraw")
        withdraw_btn.click(withdraw, inputs=withdraw_amount, outputs=[])

    with gr.Row():
        buy_symbol = gr.Textbox(label="Buy Symbol")
        buy_quantity = gr.Number(label="Buy Quantity")
        buy_btn = gr.Button("Buy Shares")
        buy_btn.click(buy_shares, inputs=[buy_symbol, buy_quantity], outputs=[])

    with gr.Row():
        sell_symbol = gr.Textbox(label="Sell Symbol")
        sell_quantity = gr.Number(label="Sell Quantity")
        sell_btn = gr.Button("Sell Shares")
        sell_btn.click(sell_shares, inputs=[sell_symbol, sell_quantity], outputs=[])

    with gr.Row():
        portfolio_btn = gr.Button("Get Portfolio")
        portfolio_output = gr.Textbox(label="Portfolio", interactive=False)
        portfolio_btn.click(get_portfolio, outputs=portfolio_output)

    with gr.Row():
        holdings_btn = gr.Button("Get Holdings")
        holdings_output = gr.Textbox(label="Holdings", interactive=False)
        holdings_btn.click(get_holdings, outputs=holdings_output)

    with gr.Row():
        transactions_btn = gr.Button("Get Transactions")
        transactions_output = gr.Textbox(label="Transactions", interactive=False)
        transactions_btn.click(get_transactions, outputs=transactions_output)

demo.launch()