import os
import json

from agents import Agent, Runner, function_tool, set_tracing_disabled

from utils import model


set_tracing_disabled(True)

class BankAccount():
    def __init__(self, name: str, pin: int, balance: int) -> None:
        self.name = name
        self.pin = pin
        self.__balance = balance
        
    @function_tool  
    def get_balance(self) -> int:
        """
        Get the balance of the bank account
        """
        return self.__balance

    @function_tool
    def deposit(self, amount: int) -> str:
        """
        Deposit money into the bank account
        """
        if amount < 1:
            return "Invalid Amount\n"
        self.__balance += amount
        return f"\n{amount} deposited successfully. Your new balance is {self.get_balance()}\n"

    @function_tool
    def withdraw(self, amount: int) -> str:
        """
        Withdraw money from the bank account
        """
        if amount > self.get_balance():
            return "Low Balance! Please enter valid amount.\n"
        
        self.__balance -= amount
        return f"\n{amount} withdrawn successfully. New balance: {self.get_balance()}\n"


account = BankAccount("Abdullah", 1111, 100000)

agent = Agent(name="ATM Machine Agent", instructions="You are an ATM machine that can deposit and withdraw money from a bank account. You can also check the balance of the account.", tools=[account.get_balance, account.deposit, account.withdraw], model=model)

runner = Runner.run_sync(agent, "Check the balance of the account")
print(runner.final_output)






