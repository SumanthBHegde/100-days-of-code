import os
import argparse


# Context Manager

class FileManager:
    def __init__(self, log_file):
        self.log_file = log_file
    
    def __enter__(self):
        """Open the log file when entering the context."""
        self.log = open(self.log_file, 'a')
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Closes the log file when entering the context"""
        if self.log:
            self.log.close()
    
    def log_operation(self, message):
        """Log the message with the timestamp"""
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.log.write(f"[{timestamp}] {message}\n")


# File Operations

def list_files(directory="."):
    """List all the files in the specified library"""
    try:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        print(f"Files in directory: {directory}")
        for file in files:
            print(file)
        return files
    except FileNotFoundError:
        print(f"Error: Directory '{directory}' not found.")
    except PermissionError:
        print(f"Error: Permission denied to access '{directory}' ")

def create_file(filename):
    """Create an empty file with given filename"""
    try:
        with open(filename, 'x') as file: # 'x' mode is for creating new file
            print(f"File '{filename}' created succesfully.")
    except FileExistsError:
        print(f"File '{filename}' already exists.")
    except Exception as e:
        print(f"An error occured: {e}")
    
def rename_file(old_name, new_name):
    """Rename a file from old_name to new_name."""
    try:
        os.rename(old_name, new_name)
        print(f"File renamed from '{old_name}' to '{new_name}'.")
    except FileNotFoundError:
        print(f"Error: File '{old_name}' not found.")
    except FileExistsError:
        print(f"A File named '{new_name}' already exists.")
    except Exception as e:
        print(f"An error occured: {e}")
        
def delete_file(filename):
    """Delete a file."""
    try:
        os.remove(filename)
        print(f"File '{filename}' deleted successfully.")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except PermissionError:
        print(f"Error: Permission denied to delete '{filename}'.")
    except Exception as e:
        print(f"An error occured: {e}")


# Permission Decorator

def require_admin(func):
    def wrapper(*args, **kwargs):
        user = kwargs.get('user', 'guest') # Simulating a user check
        if user != 'admin':
            print("Permission denied: Admin access required")
            return
        return func(*args, **kwargs)
    return wrapper

@require_admin
def delete_important_file(filename, user='guest'):
    """A sensitive file operation that requires admin access."""
    delete_file(filename)


# File Generators 

def file_generator(directory='.'):
    """Yield files from a directory one by one"""
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            yield filename
            
def main():
    parser = argparse.ArgumentParser(description="File Management System")
    
    # operations
    parser.add_argument('operation', choices=['list', 'create', 'delete', 'rename', 'log', 'generate', 'delete_admin'], help="Operation to perform")
    parser.add_argument('--filename', help="Name of the file")
    parser.add_argument('--newname', help="New name for renaming file")
    parser.add_argument('--logfile', help="Log file for context manager")
    parser.add_argument('--user', help="User to check admin permission for sensitive actions", default='guest')
    
    args = parser.parse_args()
    
    # Handle operations
    if args.operation == 'list':
        list_files(".")
    
    elif args.operation == 'create' and args.filename:
        create_file(args.filename)
    
    elif args.operation == 'delete' and args.filename:
        delete_file(args.filename)
    
    elif args.operation == 'rename' and args.filename and args.newname:
        rename_file(args.filename, args.newname)
    
    elif args.operation == 'log' and args.logfile and args.filename:
        # Test Context Manager
        with FileManager(args.logfile) as manager:
            manager.log_operation(f"Created file {args.filename}")
            create_file(args.filename)
            print(f"Logged operation in {args.logfile}")
    
    elif args.operation == 'generate':
        # Test File Generator
        print("Files generated:")
        for file in file_generator('.'):
            print(file)
    
    elif args.operation == 'delete_admin' and args.filename:
        # Test Decorator with Admin check
        delete_important_file(args.filename, user=args.user)
    
    else:
        print("Invalid arguments provided.")

if __name__ == "__main__":
    main()