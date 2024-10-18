import sqlite3
from datetime import datetime
import argparse
import requests
import schedule
import time

# Database Manager with context manager
class DatabaseManager:
    def __enter__(self):
        self.conn = sqlite3.connect('expenses.db')
        self.cursor = self.conn.cursor()
        self.create_table()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.conn.close()
    
    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT,
                amount REAL,
                category TEXT,
                date TEXT
            )
        """)
    
    def add_expense(self, description, amount, category):
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute("""
            INSERT INTO expenses (description, amount, category, date) 
            VALUES (?, ?, ?, ?)
        """, (description, amount, category, date))
        
    def view_expenses(self):
        self.cursor.execute("SELECT * FROM expenses")
        return self.cursor.fetchall()

    def delete_expense(self, expense_id):
        self.cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    
# Used only when necessary
def fetch_conversion_rate(base_currency, target_currency='INR'):
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # print("API response:", data)  Print the response for debugging
            if 'rates' in data:
                return data['rates'].get(target_currency, 1)
            else:
                print(f"Error: 'rates' not found in the response: {data}")
                return None
        else:
            print(f"Error in fetching data: {response.status_code}")
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None
    
    
def daily_summary():
    with DatabaseManager() as db:
        expenses = db.view_expenses()
        total = sum(expense[2] for expense in expenses)
        print(f"Daily Summary: Total spent today: ${total}")
    
    # Optionally, you could write the summary to file
    with open('daily_summary.txt', 'a') as log:
        log.write(f"Total spent on {datetime.now().strftime('%Y-%m-%d')}: ₹{total}\n")

def schedule_tasks():
    schedule.every().day.at("20:00").do(daily_summary)
    
    while True:
        schedule.run_pending()
        time.sleep(1)


def main():
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    parser.add_argument('operation', choices=['add', 'view', 'delete'], help="Operation to perform")
    parser.add_argument('--description', help="Expense description")
    parser.add_argument('--amount', type=float, help="Expense amount")
    parser.add_argument('--category', help="Expense category")
    parser.add_argument('--id', type=int, help="ID of the expense to delete")
    parser.add_argument('--convert', help="Convert the currency to Indian Rupees (INR)")

    args = parser.parse_args()
    
    if args.operation == 'add' and args.description and args.amount and args.category:
        if args.convert:
            conversion_rate = fetch_conversion_rate(args.convert.upper(), 'INR')
            if conversion_rate:
                converted_amount = round(args.amount * conversion_rate, 2)
                print(f"Converted amount: {converted_amount:.2f} INR (Conversion rate: {conversion_rate:.2f})")
                args.amount = converted_amount
        
        with DatabaseManager() as db:
            db.add_expense(args.description, args.amount, args.category)
        print("Expense added successfully!")
        
    elif args.operation == 'view':
        with DatabaseManager() as db:
            expenses = db.view_expenses()
            for expense in expenses:
                print(expense)
    
    elif args.operation == 'delete' and args.id:
        with DatabaseManager() as db:
            db.delete_expense(args.id)
        print(f"Expense with ID {args.id} deleted.")
    else:
        print("Invalid command or missing arguments.")


if __name__ == "__main__":
    main()
    schedule_tasks()
