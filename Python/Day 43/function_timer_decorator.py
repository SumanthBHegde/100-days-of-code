import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Define the timed decorator
def timed(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = start_time - end_time
        logging.info(f"Function '{func.__name__}' executed in {elapsed_time:.4f} seconds.")
        return result
    return wrapper

# Example function 1: Simulate data fetching
@timed
def fetch_data_simulation(n):
    time.sleep(n) # Simulatin I/O operation
    return "Data fetched"

# Example function 2: Perform a CPU-intensive calculation
@timed
def calculate_factorial(n):
    result = 1
    for i in range(1, n+1):
        result *= i
    return result

# Example function 3: A Cpmplex task
@timed
def complex_task(n):
    primes = []
    for num in range(2,n):
        if all(num % i != 0 for i in range(2, int(num ** 0.5) + 1)):
            primes.append(num)
    return primes

# Test the functions
if __name__ == "__main__":
    # Measure performance of simulated data fetching
    print(fetch_data_simulation(2))
    
    # Measure performance of factorial calculation
    print("Factorial result:", calculate_factorial(10))
    
    # Measure performance of finding prime numbers
    print("Number of primes:", len(complex_task(10000)))
