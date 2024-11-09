import random
import time
import csv
from datetime import datetime
import matplotlib.pyplot as plt

def get_temperature():
    return round(random.uniform(15.0, 35.0), 2) # In celcius

def monitor_temperature(threshold=30.0, duration=60):
    start_time = time.time()
    while time.time() - start_time < duration:
        temperature = get_temperature()
        print(f"Current Temperature: {temperature}°C")
        
        # Alert if temperature exceeds threshold
        if temperature > threshold:
            print(f"Alert! Temperature exceeded threshold: {threshold}.")
            
        # Temperature logging
        log_temperature(temperature)
            
        # Sleep for a few seconds before next reading 
        time.sleep(2)


def log_temperature(temp):
    with open("temperature_log.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), temp])

def plot_temperature():
    times = []
    temps = []
    
    # Read data from CSV
    with open("temperature_log.csv", mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            times.append(row[0])
            temps.append(float(row[1]))
    
    # Ploting 
    plt.figure(figsize=(10, 5))
    plt.plot(times, temps, label="Temperature (°C)")
    plt.xlabel("Time")
    plt.ylabel("Temperature (°C)")
    plt.title("Temperature Monitoring")
    plt.xticks(rotation=45)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # Set the threshold for temperature alerts
    threshold = 30.0
    print("Starting temperature monitoring...")
    
    # Monitor temperatures and log data for a specified duration (in seconds)
    monitor_temperature(threshold=threshold, duration=60)
    
    # Plot the recorded temperature data
    print("Temperature monitoring completed. Plotting data...")
    plot_temperature()