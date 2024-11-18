import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# List of urls to scrape
urls = [
    "https://www.example.com",
    "https://www.wikipedia.org",
    "https://www.python.org",
    "https://www.github.com",
    "https://www.stackoverflow.com"
]

# Function to fetch the content of URL
def fetch_url(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return url, response.status_code, len(response.text)
    except requests.RequestException as e:
        return url, None, f"Error: {e}"
    
# Function to scrape URLs using ThreadPoolExecutor
def scrape_urls(urls):
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(fetch_url, url): url for url in urls}
        
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
                results.append(data)
            except Exception as e:
                results.append((url, None, f"Error: {e}"))
    
    return results


# Main script
if __name__ == "__main__":
    results = scrape_urls(urls)
    
    # Print results
    for url, status, content_info in results:
        if status:
            print(f"URL: {url} | Status: {status} | Content Length: {content_info}")
        else:
            print(f"URL: {url} | Error: {content_info}")