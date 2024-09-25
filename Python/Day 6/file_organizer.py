# A program that organizes files in a given directory

import os
import shutil
from collections import defaultdict

class FileOrganizer:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.extensions_mapping = {
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
            'Documents': ['.txt', '.pdf', '.docx', '.xlsx', '.pptx'],
            'Archives': ['.zip', '.rar', '.tar', '.gz'],
            'Code': ['.py', '.js', '.html', '.css', '.cpp', '.java'],
            'Audio': ['.mp3', '.wav', '.aac'],
            'Videos': ['.mp4', '.avi', '.mkv', '.mov'],
            'Others': []
        }

        #tracking the moved files
        self.moved_files = defaultdict(int)
        self.skipped_files = 0
        
    def organize_files(self):
        
        #Ensure if the folder exists
        if not os.path.exists(self.folder_path):
            print(f"Error: The folder {self.folder_path} does not exist. ")
            return
        
        #Iterate over all the files in the directory
        for file_name in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, file_name)
            
            #Skip if its a directory
            if os.path.isdir(file_path):
                continue
            
            file_ext = os.path.splitext(file_name)[1].lower()
            folder_name = self.get_folder_name(file_ext)
            
            #Creating the folder if it doesn't exist
            if folder_name:
                target_folder = os.path.join(self.folder_path, folder_name)
                os.makedirs(target_folder, exist_ok=True)
                
                #Moving the files to the folder
                self.move_file(file_path, target_folder, file_name)
        
        self.print_summary()
    
    def get_folder_name(self, file_ext):
        for folder, extensions in self.extensions_mapping.items():
            if file_ext in extensions:
                return folder
            
        #if no matching folders put it in "Others"
        return "Others" if file_ext else None
    
    def move_file(self, file_path, target_folder, file_name):
        try:
            shutil.move(file_path, os.path.join(target_folder, file_name))
            self.moved_files[target_folder] += 1
            
        except shutil.Error as e:
            print(f"Error moving file {file_name}: {e}")
            self.skipped_files += 1
            
    def print_summary(self):
        print("\nFiles Moved:")
        for folder, count in self.moved_files.items():
            print(f"{folder}: {count} files")
        
        if self.skipped_files:
            print(f"\nFiles Skipped: {self.skipped_files}")
            
def main():
    folder_path = input("Enter the directory path to organize: ").strip()
    organizer = FileOrganizer(folder_path)
    organizer.organize_files()
    
if __name__ == "__main__":
    main()