import json

from agents import Agent, Runner, function_tool, set_tracing_disabled

from utils import model, session
from models import BankAccount


with open("accounts.json", "r") as f:
    account_data = json.load(f)


set_tracing_disabled(True)


accounts = [BankAccount(data["name"], data["pin"], data["balance"]) for data in account_data]

current_account = {"account": None}


@function_tool
def get_account(name: str, pin: int):
    """
    Get the bank account by name and pin
    """
    for account in accounts:
        if account.name == name and str(account.pin) == str(pin):
            current_account["account"] = account
            return f"Account for {name} accessed successfully."
    return "Account not found"

@function_tool
def get_balance():
    """
    Get the balance of the bank account
    """
    account = current_account["account"]
    if not account:
        return "Please login using your name and PIN first."
    return f"Your current balance is {account.balance}"


@function_tool
def deposit(amount: int) -> str:
    """
    Deposit money into the bank account
    """
    account = current_account["account"]
    if not account:
        return "Please login using your name and PIN first."
    return account.deposit(amount)


@function_tool
def withdraw(amount: int):
    """
    Withdraw money from the bank account
    """
    account = current_account["account"]
    if not account:
        return "Please login using your name and PIN first."
    return account.withdraw(amount)

@function_tool
def change_pin(prev_pin: int, new_pin: int):
    """
    Change pin by taking previous pin and new pin
    
    """
    
    account = current_account["account"]
    if not account:
        return "Please login using your name and PIN first."
    return account.change_pin(prev_pin, new_pin)

@function_tool
def greet():
    """
    Greet the user
    
    """
    
    account = current_account["account"]
    if not account:
        return "Please login using your name and PIN first."
    return account.greet()




agent = Agent(name="ATM Machine Agent", instructions="You are an ATM machine. First, use the 'get_account' tool to authenticate the user with their name and PIN and then call greet agent who will greet the user. Once authenticated and greeted, use the available tools to let users check their 1. balance, 2. deposit, or 3. withdraw money, use 4. change pin to let the user change their pin. Always ensure the account is accessed before performing any operation. Use loggins forr every action. Do not hallunicate", tools=[get_balance, deposit, withdraw, get_account, change_pin, greet], model=model)


def main():
    while True:
        try:
            user_input = input("\nSay Something: ")
            if user_input == "0":
                print("\n--Thanks for using our ATM--")
                break
            
        except:
            print("\nInvalid Input!")
            continue
            
        try:
            runner = Runner.run_sync(agent, user_input, session=session)
            print(runner.final_output)
            
        except:
            print("\nSomething went wrong")
            continue




if __name__ == "__main__":
    main()

