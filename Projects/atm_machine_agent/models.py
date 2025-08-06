import json


with open("accounts.json", "r") as f:
    account_data = json.load(f)


class BankAccount():
    def __init__(self, name: str, pin: int, balance: int) -> None:
        self.name = name
        self.__pin = pin
        self.__balance = balance
       
    @property  
    def balance(self) -> int:
        return self.__balance
    
    
    @property  
    def pin(self) -> int:
        return self.__pin
    
    
    
    def _update_account_file(self):
        for account in account_data:
            if account["name"] == self.name:
                account["pin"] = self.__pin
                account["balance"] = self.__balance
                break
        with open("accounts.json", "w") as f:
            json.dump(account_data, f, indent=4)


    def deposit(self, amount: int) -> str:
        if amount < 1:
            return "Invalid Amount\n"
        self.__balance += amount
        self._update_account_file()

        return f"\n{amount} deposited successfully. Your new balance is {self.__balance}\n"

    def withdraw(self, amount: int) -> str:
        if amount > self.__balance:
            return "Low Balance! Please enter valid amount.\n"
        
        self.__balance -= amount
    
        self._update_account_file()

        return f"\n{amount} withdrawn successfully. New balance: {self.__balance}\n"
    
    def change_pin(self, prev_pin: int, new_pin: int):
        if self.__pin != prev_pin:
            return "Previous PIN is incorrect."

        self.__pin = new_pin

        self._update_account_file()


        return "Your pin changed successfully."
    
    
    def greet(self):
        options = ["Exit", "Balance", "Deposit", "Withdraw", "Change Pin"]
        for account in account_data:
            if account["name"] == self.name and account["pin"] == self.__pin:
                print(f"\n---Welcome {account["name"]}---\n")
                for index, option in enumerate(options):
                    print(f"{index}. {option}")
                    
    
    def greet_st(self) -> str:
        return f"Welcome {self.name}!"
            
