import os
import requests
import sqlite3
import schedule
import time
from datetime import datetime
from functools import wraps

# Database Manager using context manager
class DatabaseManager:
    def __enter__(self):
        self.conn = sqlite3.connect('tasks.db')
        self.cursor  = self.conn.cursor()
        self.create_table()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.conn.close()
        
    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT,
                task_info TEXT,
                timestamp TEXT
            )
        """)
        
    def add_task(self, task_name, task_info):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute("""
            INSERT INTO tasks (task_name, task_info, timestamp) 
            VALUES (?, ?, ?) 
        """, (task_name, task_info, timestamp))
    
    def view_task(self):
        self.cursor.execute("SELECT * FROM tasks")
        return self.cursor.fetchall()
    
    def delete_task(self, task_id):
        self.cursor.execute("DELETE FROM TASKS WHERE id = ?", (task_id,))
        print(f"Task ID {task_id} deleted.")

# Admin decorator
def require_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = kwargs.get('user', 'guest') # Default user is guest
        if user != 'admin':
            print("Admin privileges required to perform this operation.")
            return
        return func(*args, **kwargs)
    return wrapper

@require_admin
def delete_task_admin(task_id, user='guest'):
    """Only admin can delete tasks."""
    with DatabaseManager() as db:
        db.delete_task(task_id)
        
# Fetch data from an API (for example quotes for adding it as task)
def fetch_daily_quote():
    url = "https://zenquotes.io/api/random"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data[0]['q'], data[0]['a']
        else:
            print("Error in fetching data: ", response.status_code)
            return None, None
    except Exception as e:
        print("An error occured: ", e)
        return None, None
    
# Scheduling tasks
def log_quote():
    """Fetch and store a quote in database"""
    quote, author = fetch_daily_quote()
    if quote and author:
        task_info = f'"{quote}" - {author}'
        with DatabaseManager() as db:
            db.add_task("Daily Quote", task_info)
        print("Quote logged: ", task_info)

# Task scheduling using the 'schedule' module
def schedule_tasks():
    schedule.every().day.at("08:00").do(log_quote) # scheduling at 8am
    
# Command line interface
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Task Automation Tool")
    parser.add_argument('operation', choices=['fetch', 'view', 'delete'], help="Operation to perform")
    parser.add_argument('--task_id', help="ID of the task to delete", type=int)
    parser.add_argument('--user', help="Specify the user type (admin/guest)")
    
    args = parser.parse_args()
    
    if args.operation == 'fetch':
        log_quote()
    elif args.operation == 'view':
        with DatabaseManager() as db:
            tasks = db.view_task()
            for task in tasks:
                print(task)
    elif args.operation == 'delete' and args.task_id:
        delete_task_admin(args.task_id, user=args.user)
    
if __name__ == "__main__":
    main()
    schedule_tasks() # Schedule tasks on script start
    while True:
        schedule.run_pending() # Keep running the scheduled tasks
        time.sleep(1)
    