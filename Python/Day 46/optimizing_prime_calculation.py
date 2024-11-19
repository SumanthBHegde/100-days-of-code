import math
import time
from concurrent.futures import ProcessPoolExecutor

# Function to check if a number is prime
def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i*i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# Function to find primes in a range
def find_primes_in_range(start, end):
    primes = [n for n in range(start, end) if is_prime(n)]
    return primes

# Single-threaded execution
def single_threaded_prime_search(range_limit):
    start_time = time.time()
    primes = find_primes_in_range(1, range_limit)
    end_time = time.time()
    print(f"Single-threaded execution time: {end_time - start_time:.2f} seconds")
    return primes

# Multi-process execution using ProcessPoolExecutor
def multi_process_prime_search(range_limit, num_processes):
    start_time = time.time()
    chunk_size = range_limit // num_processes
    ranges = [(i * chunk_size, (i + 1) * chunk_size) for i in range(num_processes)]
    ranges[-1] = (ranges[-1][0], range_limit + 1) # Enshures full range is convered
    
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        futures = [executor.submit(find_primes_in_range, start, end) for start, end in ranges]
        results = []
        for future in futures:
            results.extend(future.result())
    end_time = time.time()
    print(f"Multi-process execution time: {end_time - start_time:.2f} seconds")
    return results


# Main script
if __name__ == "__main__":
    RANGE_LIMIT = 1_000_000
    NUM_PROCESSES = 4

    print("Calculating primes with a single thread...")
    single_threaded_primes = single_threaded_prime_search(RANGE_LIMIT)

    print("\nCalculating primes with multiple processes...")
    multi_process_primes = multi_process_prime_search(RANGE_LIMIT, NUM_PROCESSES)

    # Validate results
    print("\nValidation:")
    print(f"Single-threaded primes count: {len(single_threaded_primes)}")
    print(f"Multi-process primes count: {len(multi_process_primes)}")
    print(f"Results match: {set(single_threaded_primes) == set(multi_process_primes)}")