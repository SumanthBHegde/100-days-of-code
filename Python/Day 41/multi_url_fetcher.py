import time
import requests
from concurrent.futures import ThreadPoolExecutor

# List of URLs for testing
urls = [
    "https://jsonplaceholder.typicode.com/posts",
    "https://jsonplaceholder.typicode.com/comments",
    "https://jsonplaceholder.typicode.com/albums",
    "https://jsonplaceholder.typicode.com/photos",
]

# Function to fetch data from a URL
def fetch_url(url):
    try:
        response = requests.get(url)
        return response.status_code, url
    except requests.RequestException as e:
        return None, f"Error fetching {url}: {e}"
    
# Sequential fetch
def fetch_sequential(urls):
    results = []
    start_time = time.time()
    for url in urls:
        results.append(fetch_url(url))
    end_time = time.time()
    print(f"Sequential Execution TimeL {end_time - start_time:.2f} seconds")
    return results

# Multithreaded fetch
def fetch_multithreaded(urls):
    results = []
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=len(urls)) as executor:
        results = list(executor.map(fetch_url, urls))
    end_time = time.time()
    print(f"Multithreaded Execution TimeL {end_time - start_time:.2f} seconds")
    return results

# Run both methods
print("Sequential Fetching Results: ")
sequential_results = fetch_sequential(urls)
for status, url in sequential_results:
    print(f"{url}: {status}")

print("\nMultithreaded Fetching Results: ")
multithreaded_results = fetch_multithreaded(urls)
for status, url in multithreaded_results:
    print(f"{url}: {status}")