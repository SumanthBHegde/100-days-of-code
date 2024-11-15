import time
import multiprocessing

# List of large numbers for factorial calculation
numbers = [5000, 1000, 1500, 2000]

# Function to calculate factorial of a number
def factorial(n):
    result = 1
    for i in range(1, n+1):
        result *= i
    return result

# Sequential factorial calculation
def factorial_sequential(numbers):
    results = []
    start_time = time.time()
    for num in numbers:
        results.append(factorial(num))
    end_time = time.time()
    print(f"Sequential Execution Time: {end_time - start_time:.2f} seconds")
    return results

# Multiprocessing factorial calculation
def factorial_multiprocessing(numbers):
    start_time = time.time()
    with multiprocessing.Pool(processes=len(numbers)) as pool:
        results = pool.map(factorial, numbers)
    end_time = time.time()
    print(f"Multiprocessing Execution Time: {end_time - start_time:.2f} seconds")
    return results

# Run both methods
print("Sequential Factorial Results: ")
sequential_results = factorial_sequential(numbers)
print(sequential_results)

print("\nMultiprocessing Factorial Results: ")
multiprocessing_results = factorial_multiprocessing(numbers)
print(multiprocessing_results)