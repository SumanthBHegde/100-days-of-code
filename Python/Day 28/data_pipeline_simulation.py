import random
import time

class DataSource:
    def __init__(self):
        self.data = []
    
    def generate_data(self, num_points=10):
        self.data = [random.randint(1,100) for _ in range(num_points)]
        print(f"DataSource generated data: {self.data}")
        return self.data
    

class DataProcessor:
    def __init__(self):
        self.processed_data = []
    
    def process_data(self, data):
        self.processed_data = [x**2 for x in data]
        print(f"DataProcessor processed data: {self.processed_data}")
        return self.processed_data
    
    
class DataStorage:
    def __init__(self):
        self.storage = []
    
    def store_data(self, data):
        self.storage.extend(data)
        print(f"DataStorage current storage: {self.storage}")
    
    def retrieve_data(self):
        print(f"DataStorage retrieved data: {self.storage}")
        return self.storage


class DatalPipeline:
    def __init__(self, source, processor, storage):
        self.source = source
        self.processor = processor
        self.storage = storage
        
    def run_pipeline(self):
        print("Running data pipeline....")
        raw_data = self.source.generate_data()
        processed_data = self.processor.process_data(raw_data)
        self.storage.store_data(processed_data)
        print("Data pipeline run complete.")
    
# Instantiate the components
data_source = DataSource()
data_processor = DataProcessor()
data_storage = DataStorage()

# Create the pipeline
pipeline = DatalPipeline(data_source, data_processor, data_storage)

# Run the pipeline
pipeline.run_pipeline()

# Retrieve and display the stored data
data_storage.retrieve_data()
    