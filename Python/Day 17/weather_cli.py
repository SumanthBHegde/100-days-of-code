import sqlite3
import requests
from dotenv import load_dotenv
import os
import argparse

# Setting up dotenv
load_dotenv()

API_KEY = os.getenv('WEATHER_API_KEY')

if not API_KEY:
    print("Api key not found(server).")


class DatabaseManager:
    """Context Manager for database connections"""
    
    def __init__(self, db_name='weather.db'):
        self.db_name = db_name
    
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_table()
        return self.cursor
    
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_value is None:
            self.conn.commit()
        self.conn.close()
        
    
    def create_table(self):
        """Creates the weather table if it doesn't exist."""
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT UNIQUE,
            temperature REAL,
            humidity INTEGER,
            description TEXT
            )
        """)

def fetch_weather(city):
    """Fetch the weather data for the given city."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        weather_data = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"]
        }
        return weather_data
    else:
        print(f"Error: Unable to fetch weather for {city}")
        return None
    
def store_weather_data(weather_data):
    """Storing weather data in the sqlite"""
    with DatabaseManager() as db:
        db.execute("""
            INSERT OR REPLACE INTO weather (city, temperature, humidity, description)
            VALUES (?,?,?,?)
        """, (weather_data['city'], weather_data['temperature'], weather_data['humidity'], weather_data['description']))
        print(f"Weather data for {weather_data['city']} stored successfully")
        
def view_weather_data(city):
    """View weather data for a given city from the database."""
    with DatabaseManager() as db:
        db.execute("SELECT * FROM weather WHERE city=?", (city,))
        row = db.fetchone()
        if row:
            print(f"City: {row[1]}\nTemperature: {row[2]}°C\nHumidity: {row[3]}%\nDescription: {row[4]}")
        else:
            print(f"No data found for {city}") 
        
def update_weather_data(city):
    """Upadate the weather data for a city"""
    weather_data = fetch_weather(city)
    if weather_data:
        store_weather_data(weather_data)

def delete_weather_data(city):
    """Delete weather data for a city from the database"""
    with DatabaseManager() as db:
        db.execute("DELETE FROM weather WHERE city=?", (city,))
        print(f"Weather data for {city} deleted successfully.")

def main():
    parser = argparse.ArgumentParser(description="Weather Application")
    parser.add_argument('operation', choices=['fetch', 'view', 'update', 'delete'], help="Operation to perform")
    parser.add_argument('--city', help="City to fetch/view/update/delete weather data")
    
    args = parser.parse_args()
    
    if args.operation == 'fetch' and args.city:
        weather_data = fetch_weather(args.city)
        if weather_data:
            store_weather_data(weather_data)

    elif args.operation == 'view' and args.city:
        view_weather_data(args.city)

    elif args.operation == 'update' and args.city:
        update_weather_data(args.city)

    elif args.operation == 'delete' and args.city:
        delete_weather_data(args.city)

    else:
        print("Invalid arguments provided.")

if __name__ == "__main__":
    main()