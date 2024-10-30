import csv
import os
from collections import defaultdict

class DataPipeline:
    def __init__(self):
        self.data = []
        self.header = []
        
    def load_data(self, file_path):
        if not os.path.exists(file_path):
            print("File not found")
            return
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            self.header = reader.fieldnames
            self.data = [row for row in reader]
        print("Data loaded successfully.")
    
    def display_data(self, n=5):
        """Display the first n rows of data."""
        if not self.data:
            print("No data to display.")
            return
        print(self.header)
        for row in self.data[:n]:
            print(row)
            
    def clean_data(self):
        # Remove duplicates (using a set if rows are hashable dictionaries)
        seen = set()
        unique_data = []
        for row in self.data:
            row_tuple = tuple(row.items())  
            if row_tuple not in seen:
                seen.add(row_tuple)
                unique_data.append(row)
        
        # Update self.data with unique rows
        self.data = unique_data

        # Handle missing values by removing rows with any None or empty values
        self.data = [row for row in self.data if all(value not in [None, ''] for value in row.values())]
    
    def transform_data(self):
        """Add new coloumns or perform calculations on the data."""
        
        # Example: Calculate "salary_category" based on the salary
        for row in self.data:
            salary = int(row['salary']) if row['salary'].isdigit() else 0
            if salary >= 80000:
                row["salary_category"] = "High"
            elif salary >= 60000:
                row["salary_category"] = "Medium"
            else:
                row["salary_category"] = "Low"
        print("Data Transformed successfully.")
        
    def save_data(self, output_path):
        """Save processed data to a new .csv file."""
        
        with open(output_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.header + ['salary_category'])
            writer.writeheader()
            writer.writerows(self.data)
        print(f"Data saved to {output_path}.")
        
    def show_menu(self):
        """Show menu options for the CLI."""
        
        print("\nChoose an option:")
        print("1. Load Data")
        print("2. Display Data")
        print("3. Clean Data")
        print("4. Transform Data")
        print("5. Save Data")
        print("6. Exit")
    
    def run(self):
        """Run the data pipeline CLI."""
        
        while True:
            self.show_menu()
            choice = input("Enter your choice: ").strip()
            if choice == "1":
                file_path = input("Enter the path to the CSV file: ").strip()
                self.load_data(file_path)
            elif choice == "2":
                n = int(input("Enter the number of rows to display: "))
                self.display_data(n)
            elif choice == "3":
                self.clean_data()
            elif choice == "4":
                self.transform_data()
            elif choice == "5":
                output_path = input("Enter the path to save the processed data: ").strip()
                self.save_data(output_path)
            elif choice == "6":
                print("Exiting the pipeline.")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    pipeline = DataPipeline()
    pipeline.run()