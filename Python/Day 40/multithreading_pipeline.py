import os
import threading
import multiprocessing
import logging
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from contextlib import contextmanager

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Directory to store data files
DATA_DIR = "dir"
PROCESSED_DIR = "processed_data"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

# Custom Exception for invalid data
class InvalidDataException(Exception):
    pass

# Context Manager for file handling
@contextmanager
def open_file(file_path, mode):
    try:
        file = open(file_path, mode)
        yield file
    finally:
        file.close()

# Data extraction simulation
def simulate_data_download(file_num):
    filename = f"{DATA_DIR}/data_file{file_num}.txt"
    with open_file(filename, 'w') as f:
        f.write("This is simple data for file "+ str(file_num) * 100) # simulating large data
    logging.info(f"Downloaded file {filename}")

# Parallel data processing function
def process_data_file(file_name):
    try:
        with open_file(f"{DATA_DIR}/{file_name}", 'r') as f:
            data = f.read()
        
        # basic validation
        if len(data) < 50: # arbitrary length check for example
            raise InvalidDataException(f"{file_name} has insufficient data.")
        
        # basic data processing 
        processed_data = ''.join(set(data.split()))
        
        # Save processed data
        with open_file(f"{PROCESSED_DIR}/{file_name}", 'w') as f:
            f.write(processed_data)
        
        logging.info(f"Processsed file {file_name}")
    
    except InvalidDataException as e:
        logging.error(e)
    except Exception as e:
        logging.error(f"Unexpected error processing {file_name}: {e}")

# Downloading files with multithreading
def download_data_files(num_files):
    with ThreadPoolExecutor() as executor:
        executor.map(simulate_data_download, range(num_files))

# Processing files with multiprocessing
def process_all_data_files():
    files = os.listdir(DATA_DIR)
    with ProcessPoolExecutor() as executor:
        executor.map(process_data_file, files)

# Main Pipeline Execution
if __name__ == "__main__":
    # Download data files
    logging.info("Starting data download....")
    download_data_files(10)
    
    # Process data files
    logging.info("Starting data processing....")
    process_all_data_files()
    
    logging.info("Pipeline execution completed.")