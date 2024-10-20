import sqlite3
import os
import random
import string
from cryptography.fernet import Fernet
import argparse
import getpass

# Encrytion Helper Functions

def generate_key():
    """ Key generation and saving it to a file for later use """
    key = Fernet.generate_key()
    with open('secret.key', 'wb') as key_file:
        key_file.write(key)

def load_key():
    """Load the key from the secret.key file"""
    return open("secret.key", "rb").read()

def encrypt_password(password):
    """Encrypt the password"""
    key = load_key()
    cipher = Fernet(key)
    encrypted_password = cipher.encrypt(password.encode())
    return encrypted_password

def decrypt_password(password):
    """Decrypt the password"""
    key = load_key()
    cipher = Fernet(key)
    decrypted_password = cipher.decrypt(password).decode()
    return decrypted_password


# Password Generation

def generate_password(length=12, include_sqecial_chars=True):
    """Generate a random password"""
    chars = string.ascii_letters + string.digits
    if include_sqecial_chars:
        chars += string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))
    return password


# Database Manager

class DatabaseManager:
    def __enter__(self):
        self.conn = sqlite3.connect('passwords.db')
        self.cursor = self.conn.cursor()
        self.create_table()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.conn.close()
    
    def create_table(self):
        """Creating a table if it dosen't exist"""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            password BLOB NOT NULL,
            added_on TEXT NOT NULL
        )''')
        
    def add_password(self, website, username, password):
        """Add a new password entry"""
        encrypted_password = encrypt_password(password)
        self.cursor.execute("""
            INSERT INTO passwords (website, username, password, added_on)
            VALUES (?, ?, ?, datetime('now'))
        """, (website, username, encrypted_password))
    
    def view_passwords(self):
        """View all password entries"""
        self.cursor.execute('SELECT * FROM passwords')
        return self.cursor.fetchall()
    
    def retrieve_password(self, website):
        """Retrieve a password for a specific website"""
        self.cursor.execute('SELECT username, password FROM passwords WHERE website = ?', (website,))
        result = self.cursor.fetchone()
        if result:
            username, encrypted_password = result
            decrypted_password = decrypt_password(encrypted_password)
            return username, decrypted_password
        else:
            return None, None
    
    def update_password(self, website, new_password):
        """Update a password for a specific website"""
        encrypted_password = encrypt_password(new_password)
        self.cursor.execute('UPDATE passwords SET password = ? WHERE website = ?', (encrypted_password, website))
        
    def delete_password(self, website):
        """Delete a password for a specific website"""
        self.cursor.execute('DELETE FROM passwords WHERE website = ?', (website,))
        

# CLI Interface
def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description="Password Manager")

    subparsers = parser.add_subparsers(dest="command")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new password")
    add_parser.add_argument("--website", required=True, help="Website name")
    add_parser.add_argument("--username", required=True, help="Username for the website")
    add_parser.add_argument("--password", help="Password (if not provided, will generate one)")

    # View command
    view_parser = subparsers.add_parser("view", help="View all passwords")

    # Retrieve command
    retrieve_parser = subparsers.add_parser("retrieve", help="Retrieve a password")
    retrieve_parser.add_argument("--website", required=True, help="Website name")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update an existing password")
    update_parser.add_argument("--website", required=True, help="Website name")
    update_parser.add_argument("--password", required=True, help="New password")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a password")
    delete_parser.add_argument("--website", required=True, help="Website name")

    args = parser.parse_args()

    if args.command == "add":
        website = args.website
        username = args.username
        password = args.password if args.password else generate_password()
        with DatabaseManager() as db:
            db.add_password(website, username, password)
        print(f"Password added for {website}.")
        if not args.password:
            print(f"Generated password: {password}")

    elif args.command == "view":
        with DatabaseManager() as db:
            records = db.view_passwords()
            for re in records:
                print(f"ID: {re[0]}, Website: {re[1]}, Username: {re[2]}, Added On: {re[4]}")

    elif args.command == "retrieve":
        website = args.website
        with DatabaseManager() as db:
            username, password = db.retrieve_password(website)
            if username:
                print(f"Website: {website}\nUsername: {username}\nPassword: {password}")
            else:
                print(f"No password found for {website}.")

    elif args.command == "update":
        website = args.website
        new_password = args.password
        with DatabaseManager() as db:
            db.update_password(website, new_password)
        print(f"Password updated for {website}.")

    elif args.command == "delete":
        website = args.website
        with DatabaseManager() as db:
            db.delete_password(website)
        print(f"Password deleted for {website}.")

if __name__ == "__main__":
    if not os.path.exists("secret.key"):
        generate_key()
    main()
        