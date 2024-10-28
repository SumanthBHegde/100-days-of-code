class BankAccount:
    def __init__(self, account_number, initial_balance=0):
        self.__account_number = account_number
        self.__balance = initial_balance
    
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"Deposit successful. New balance: {self.__balance}")
        else:
            print("Invalid deposit amount.")
    
    def withdraw(self, amount):
        if amount <= self.__balance:
            self.__balance -= amount
            print(f"Withdrawal successful. New balance:{self.__balance}")
            
    def get_balance(self):
        return self.__balance
    
    def get_account_number(self):
        return self.__account_number


class SavingsAccount(BankAccount):
    def __init__(self, account_number, initial_balance=0, interest_rate=0.02):
        super().__init__(account_number, initial_balance)
        self.interest_rate = interest_rate
        
    def apply_interest(self):
        interest = self.get_balance() * self.interest_rate
        self.deposit(interest)
        print(f"Intrest applied. New Balance {self.get_balance()}")
    

class CheckingAccount(BankAccount):
    def __init__(self, account_number, initial_balance=0, overdraft_limit=0):
        super().__init__(account_number, initial_balance)
        self.overdraft_limit = overdraft_limit
    
    def withdraw(self, amount):
        if amount <= self.get_balance() + self.overdraft_limit:
            new_balance = self.get_balance() - amount
            if new_balance < 0:
                print(f"Withdrawal allowed with overdraft. New balance: {new_balance}")
            else:
                print(f"Withdrwal successful. New balance: {new_balance}")
            self.BankAccount__balance = new_balance
        else:
            print("Withdrawal exceeds overdraft limit.")

def process_account(account, action, amount=None):
    if action == "deposit" and amount is not None:
        account.deposit(amount)
    elif action == "withdraw" and amount is not None:
        account.withdraw(amount)
    elif action == "apply_interest" and isinstance(account, SavingsAccount):
        account.apply_interest()
    else:
        print("Invalid action or account type.")

if __name__ == "__main__":
    # Create a savings and checking account
    savings = SavingsAccount("001", 1000, 0.03)
    checking = CheckingAccount("002", 500, 200)

    # Test deposits and interest application on savings
    savings.deposit(200)
    savings.apply_interest()

    # Test withdrawal with overdraft on checking
    checking.withdraw(600)  # Should allow overdraft up to limit

    # Test process_account function with polymorphism
    process_account(savings, "apply_interest")
    process_account(checking, "withdraw", 100)