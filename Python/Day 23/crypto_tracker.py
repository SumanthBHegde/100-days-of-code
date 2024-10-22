import requests
import argparse
import json
import csv
import os 
import sqlite3
from datetime import datetime

API_URL = "https://api.coingecko.com/api/v3/simple/price"
DATABASE_FILE = 'crypto_prices.db'


def fetch_crypto_prices(cryptos, vs_currency='inr'):
    """Fetch the current prices of multiple cryptocurrencies"""
    try: 
        response = requests.get(API_URL, params={'ids': ','.join(cryptos), 'vs_currencies': vs_currency})
        data = response.json()
        return {crypto : data.get(crypto, {}).get(vs_currency) for crypto in cryptos}
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def save_prices_to_csv(cryptos, prices, vs_currency='inr'):
    """Save prices to a csv file with timestamps"""
    file_exists = os.path.isfile('crypto_prices.csv')
    with open('crypto_prices.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            # Write the header if file is new
            writer.writerow(['Timestamp', 'Cryptocurrency', 'Price', 'Currency'])
        for crypto in cryptos:
            writer.writerow([datetime.now(), crypto, prices[crypto], vs_currency])
    print("Prices saved to crypto_prices.csv")
    

def setup_database():
    """Create the sqlite database and table if they don't exist"""
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prices (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            crypto TEXT NOT NULL,
                            price REAL NOT NULL,
                            currency TEXT NOT NULL,
                            timestamp TEXT NOT NULL)''')
        conn.commit()
        

def save_prices_to_db(cryptos, prices, vs_currency='inr'):
    """Saving prices to database"""
    timestamp = datetime.now().isoformat()
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        for crypto in cryptos:
            cursor.execute("INSERT INTO prices (crypto, price, currency, timestamp) VALUES (?, ?, ?, ?)",
                           (crypto, prices[crypto], vs_currency, timestamp))
        conn.commit()
    print("Prices saved to database.")


def retrieve_price_history(crypto):
    """Retrieve historical prices for a specific cryptocurrency from the database."""
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM prices WHERE crypto = ? ORDER BY timestamp DESC", (crypto,))
        records = cursor.fetchall()
        if records:
            for record in records:
                print(f"{record[4]} - {record[1]}: {record[2]} {record[3]}")
        else:
            print(f"No price history available for {crypto}.")

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description="Cryptocurrency Price Tracker")
    
    subparsers = parser.add_subparsers(dest="command")

    # Add command for fetching current prices
    price_parser = subparsers.add_parser("fetch", help="Fetch current cryptocurrency prices")
    price_parser.add_argument('--crypto', required=True, help="Cryptocurrency symbols (comma-separated)")
    price_parser.add_argument('--currency', default='inr', help="Fiat currency (default: INR)")
    price_parser.add_argument('--store', choices=['csv', 'db'], help="Store fetched prices in CSV or SQLite")

    # Add command for retrieving price history
    history_parser = subparsers.add_parser("history", help="Retrieve price history")
    history_parser.add_argument('--crypto', required=True, help="Cryptocurrency symbol for history retrieval")

    args = parser.parse_args()
    
    if args.command == "fetch":
        # Fetch prices
        cryptos = args.crypto.split(',')
        currency = args.currency.lower()
        
        prices = fetch_crypto_prices(cryptos, vs_currency=currency)
        
        if prices:
            for crypto in cryptos:
                print(f"The current price of {crypto.capitalize()} is {prices[crypto]} {currency.upper()}.")

            # store prices if requested
            if args.store == 'csv':
                save_prices_to_csv(cryptos, prices, vs_currency=currency)
            elif args.store == 'db':
                setup_database()
                save_prices_to_db(cryptos, prices, vs_currency=currency)
            
        elif args.command == 'history':
            # Retrieve price history
            crypto = args.crypto.lower()
            retrieve_price_history(crypto)
            

if __name__ == "__main__":
    main()
                
        