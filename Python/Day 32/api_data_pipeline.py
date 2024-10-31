import requests
import csv

class APIDataPipeline:
    def __init__(self, api_url):
        self.api_url = api_url
        self.data = []
    
    def fetch_data(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            self.data = response.json()
            print("Data fetched successfully.")
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            
    def clean_data(self):
        if not self.data:
            print("No data to clean.")
            return
        
        cleaned_data = []
        for entry in self.data:
            # Only keep relevant fields from each user 
            if "id" in entry and "name" in entry:
                cleaned_data.append({
                    "id": entry['id'],
                    "name": entry['name'],
                    "username": entry.get("username", "N/A"),
                    "email": entry.get("email", "N/A"),
                    "city": entry.get("address", {}).get("city", "N/A")
                })
            self.data = cleaned_data
            print("Data cleaned successfully.")
            
    def save_to_csv(self, filename):
        if not self.data:
            print("No data found.")
            return
        
        try:
            fieldnames = ["id", "name", "username", "email", "city"]
            with open(filename, mode='w', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.data)
            print(f"Data saved to {filename} successfully.")
        except IOError as e:
            print(f"Error saving data: {e}")
            
if __name__ == "__main__":
    api_url = "https://jsonplaceholder.typicode.com/users"
    pipeline = APIDataPipeline(api_url)
    pipeline.fetch_data()
    pipeline.clean_data()
    pipeline.save_to_csv("users.csv")