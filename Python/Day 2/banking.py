# A simple banking app to learn about python

class Account:
    account_counter = 10000
    
    def __init__(self):
        Account.account_counter += 1
        self.account_number = Account.account_counter
        self.balance = 0
        self.transaction_history = []
    
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(f"Deposit: {amount}")
            print(f"Deposit succesful. New balance: {self.balance}")
        else:
            print("Invalid Deposit Amount")
    
    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            self.transaction_history.append(f"Withdraw: {amount}")
            print(f"Widthdraw succesful. New balance: {self.balance}")
        else:
            print("Invalid or Insufficient funds for withdrawl.")
    
    def view_balance(self):
        print(f"Current: {self.balance}")
    
    def view_transaction_history(self):
        print("Transaction history: ")
        for i, transaction in enumerate(self.transaction_history, start=1):
            print(f"{i}. {transaction}")
    

class Bank:
    def __init__(self):
        self.accounts = {}
    
    def create_account(self):
        account = Account()
        self.accounts[account.account_number] = account
        print(f"Account created. Your account number is: {account.account_number}")
        
    def get_account(self, account_number):
        return self.accounts.get(account_number)
    
    def deposit(self, account_number, amount):
        account = self.get_account(account_number)
        if account:
            account.deposit(amount)
        else:
            print("Account not found.")
            
    def withdraw(self, account_number, amount):
        account = self.get_account(account_number)
        if account:
            account.withdraw(amount)
        else:
            print("Account not found.")
            
    def view_balance(self, account_number):
        account = self.get_account(account_number)
        if account:
            account.view_balance()
        else:
            print("Account not found.")
    
    def view_transaction_history(self, account_number):
        account = self.get_account(account_number)
        if account:
            account.view_transaction_history()
        else:
            print("Account not found.")

def main():
    bank = Bank()

    while True:
        print("\nChoose an option to perform operation\n 1. Create Account\n 2. Deposit\n 3. Withdraw\n 4. View Balance\n 5. View Transaction History\n 6. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            bank.create_account()
        elif choice == '2':
            account_number = int(input("Enter account number: "))
            amount = float(input("Enter amount to deposit: "))
            bank.deposit(account_number, amount)
        elif choice == '3':
            account_number = int(input("Enter account number: "))
            amount = float(input("Enter amount to withdraw: "))
            bank.withdraw(account_number, amount)
        elif choice == '4':
            account_number = int(input("Enter account number: "))
            bank.view_balance(account_number)
        elif choice == '5':
            account_number = int(input("Enter account number: "))
            bank.view_transaction_history(account_number)
        elif choice == '6':
            print("Thank you for your patience!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()