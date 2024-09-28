import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Function to get the weather data
def get_weather(city_name, api_key, units):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    forecast_url = "http://api.openweathermap.org/data/2.5/forecast?"
    
    #Set the correct unit for temperature display
    unit_symbol = '°C' if units == 'metric' else '°F'
    
    #Complete URLs for current weather
    complete_weather_url = f"{base_url}q={city_name}&appid={api_key}&units={units}"
    complete_forecast_url = f"{forecast_url}q={city_name}&appid={api_key}&units={units}"
    
    try:
        # Get current weather data
        weather_response = requests.get(complete_weather_url)
        weather_data = weather_response.json()
        
        # Handle cases for invalid city name or API issues
        if weather_data['cod'] != 200:
            print(f"Error: {weather_data.get('message', 'City not found.')}\n")
            return
        
        # Extract and display current weather
        main_data = weather_data['main']
        weather_description = weather_data['weather'][0]['description']
        wind_speed = weather_data['wind']['speed']
        
        print(f"\nCurrent Weather for {city_name.capitalize()}:")
        print(f"Temperature: {main_data['temp']}{unit_symbol}")
        print(f"Weather: {weather_description.capitalize()}")
        print(f"Humidity: {main_data['humidity']}%")
        print(f"Wind Speed: {wind_speed} m/s\n")
        
        # Fetch and display 5-day weather forecast
        forecast_response = requests.get(complete_forecast_url)
        forecast_data = forecast_response.json()
        
        print(f"5-Day Weather Forecast for {city_name.capitalize()}:\n")
        
        # Loop through the forecast data (every 3 hours)
        for forecast in forecast_data['list']:
            time = forecast['dt_txt']
            temp = forecast['main']['temp']
            description = forecast['weather'][0]['description']
            print(f"{time} - Temp: {temp}{unit_symbol}, Weather: {description.capitalize()}")
            
    except requests.exceptions.RequestException as e:
        print(f"Network error occured on {e} ")
    except KeyError:
        print("Invalid API Key or data found.")
    except Exception as e:
        print(f"An Error occured: {e}\n")
        
# Main function to get the user input
def main():
    
    #load api key
    api_key = os.getenv('WEATHER_API_KEY')
    
    if not api_key:
        print("Api key not found(server).")
        return
    
    while True:
        city_name = input("Enter city name (or type 'exit' to quit): ").strip()
        if city_name.lower() == 'exit':
            break
        
        # Choose temperature unit (Celsius or Fahrenheit)
        unit_choice = input("Choose temperature unit: (C) Celsius or (F) Fahrenheit: ").strip().lower()
        if unit_choice == 'c':
            units = 'metric'
        elif unit_choice == 'f':
            units = 'imperial'
        else:
            print("Invalid choice. Using Celsius by default.\n")
            units = 'metric'
        
        # Fetch and display weather data (current + 5-day forecast)
        get_weather(city_name, api_key, units)

if __name__ == "__main__":
    main()