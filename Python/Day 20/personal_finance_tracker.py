import sqlite3
from datetime import datetime
import argparse
import matplotlib.pyplot as plt
import csv

# Database Manager
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
                amount REAL,
                category TEXT,
                description TEXT,
                date TEXT
            )
        """)
    
    def add_expense(self, amount, category, description):
        date = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        self.cursor.execute("""
            INSERT INTO expenses (amount, category, description, date)
            VALUES (?,?,?,?)
        """, (amount, category, description, date))
        
    def get_expenses(self):
        self.cursor.execute('SELECT * FROM expenses')
        return self.cursor.fetchall()
    
    def get_expenses_by_category(self):
        self.cursor.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
        return self.cursor.fetchall()
    
    def get_expenses_by_date(self):
        self.cursor.execute('SELECT date, SUM(amount) FROM expenses GROUP BY date')
        return self.cursor.fetchall()


# Visualization using matplotlib
def visualize_expenses():
    with DatabaseManager() as db:
        expenses_by_category = db.get_expenses_by_category()
        
        categories = [row[0] for row in expenses_by_category]
        amounts = [row[1] for row in expenses_by_category]
        
        # Pie chart for categories
        plt.figure(figsize=(8,8))
        plt.pie(amounts, labels=categories, autopct='%1.1f%%')
        plt.title("Expenses by Category")
        plt.show()
        
        # Bar chart
        plt.figure(figsize=(10,5))
        plt.bar(categories, amounts, color='skyblue')
        plt.title("Expenses by Category (Bar Chart)")
        plt.ylabel('Amount')
        plt.show()
        
        # Line graph for expense trend over time
        expenses_by_date = db.get_expenses_by_date()
        date_time = [datetime.strptime(row[0], '%d/%m/%Y %H:%M:%S') for row in expenses_by_date]
        dates = [date.date() for date in date_time]  
        
        amounts_by_date = [row[1] for row in expenses_by_date]
        
        plt.figure(figsize=(10,5))
        plt.plot(dates, amounts_by_date, marker='o', linestyle='-', color='green')
        plt.title("Expense Trend Over Time")
        plt.xlabel("Date")
        plt.ylabel("Amount")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

def export_to_csv():
    with DatabaseManager() as db:
        expenses = db.get_expenses()
        
        with open('expenses.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Amount", "Category", "Description", "Date"])
            writer.writerows(expenses)
        
        print("Data exported to expenses.csv")

# CLI for tracker
def main():
    parser = argparse.ArgumentParser(description="Personal Finance Tracker")
    
    parser.add_argument('operation', choices=['add', 'summary', 'visualize', 'export'],
                        help="Operation to perform: add, summary, visualize, export")

    parser.add_argument('--amount', type=float, help="Amount for the expense")
    parser.add_argument('--category', type=str, help="Category for the expense (e.g., food, travel)")
    parser.add_argument('--description', type=str, help="Description of the expense")
    
    args = parser.parse_args()
    
    if args.operation == 'add' and args.amount and args.category:
        with DatabaseManager() as db:
            db.add_expense(args.amount, args.category, args.description)
            print(f"Expense added: {args.amount} to {args.category}")
        
    elif args.operation == 'summary':
        with DatabaseManager() as db:
            expenses = db.get_expenses()
            for expense in expenses:
                print(expense)
    
    elif args.operation == 'visualize':
        visualize_expenses()
    
    elif args.operation == 'export':
        export_to_csv()

if __name__ == "__main__":
    main()