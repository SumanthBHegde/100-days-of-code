import sqlite3
from contextlib import contextmanager

# Define a custom context manager for database connection
@contextmanager
def database_connection(db_name):
    connection = None
    try:
        # Establish connection
        connection = sqlite3.connect(db_name)
        print(f"Connected to database: {db_name}")
        yield connection
    except Exception as e:
        print(f"An error occured: {e}")
    finally:
        if connection:
            connection.close()
            print(f"Database connection to {db_name} closed")

# Example usage
if __name__ == "__main__":
    
    # Defining dummy database name
    db_name = "test_database.db"
    
    # Create a table and insert some data
    with database_connection(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER
        )
        """)
        print("Table created successfully.")

        cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 30))
        cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Bob", 25))
        conn.commit()
        print("Data inserted successfully.")
        
    # Query data from the table
    with database_connection(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        print("Users in database: ")
        for row in rows:
            print(row)
    