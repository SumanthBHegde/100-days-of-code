#Student Gradebook System with File Handling

import os
import json

class Gradebook:
    def __init__(self, filename):
        self.filename = filename
        self.gradebook = self.load_gradebook()
        
    def load_gradebook(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load()
        else:
            return {}
        
    def save_gradebook(self):
        with open(self.filename, 'w') as f:
            json.dump(self.gradebook, f, indent=1)
    
    def add_student(self, name, subjects_grades):
        if name in self.gradebook:
            print("Student already exists!")
        else:
            self.gradebook[name] = subjects_grades
            print(f"Student {name} added succesfully.")
            
    def update_student(self, name, subjects_grades):
        if name in self.gradebook:
            self.gradebook[name].update(subjects_grades)
            print(f"Grades updated for {name}!")
        else:  
            print("Student not found.")
        
    def delete_student(self, name):
        if name in self.gradebook:
            del self.gradebook[name]
            print(f"Student {name} deleted!")
        else:  
            print("Student not found.")
    
    def view_grades(self, name):
        if name in self.gradebook:
            print(f"{name}'s Grades:")
            for subject, grade in self.gradebook[name].items():
                print(f" - {subject}: {grade}")
        else:
            print("Student not found.")
    
    def calculate_average(self, name):
        if name in self.gradebook:
            grades = list(self.gradebook[name].values())
            avg = sum(grades)/len(grades)
            cgpa = (avg/100)*10
            print(f"Average grade for {name}: {avg:.2f}")
            print(f"CGPA for {name}: {cgpa:.2f}")
        else:
            print("Student not found.")
    
def main():
    gradebook = Gradebook("gradebook.json")

    while True:
        print("\n1. Add Student\n2. Update Grades\n3. Delete Student\n4. View Student Grades")
        print("5. Calculate Average Grade\n6. Save & Exit")

        choice = input("Choose an option: ").strip()

        if choice == '1':
            name = input("Enter student name: ")
            subjects = input("Enter subjects and grades (e.g., Math:90, Science:85): ")
            subjects_grades = dict(item.split(":") for item in subjects.split(", "))
            subjects_grades = {k: int(v) for k, v in subjects_grades.items()}
            gradebook.add_student(name, subjects_grades)

        elif choice == '2':
            name = input("Enter student name: ")
            subjects = input("Enter subjects and grades to update (e.g., Math:95): ")
            subjects_grades = dict(item.split(":") for item in subjects.split(", "))
            subjects_grades = {k: int(v) for k, v in subjects_grades.items()}
            gradebook.update_grades(name, subjects_grades)

        elif choice == '3':
            name = input("Enter student name: ")
            gradebook.delete_student(name)

        elif choice == '4':
            name = input("Enter student name: ")
            gradebook.view_grades(name)

        elif choice == '5':
            name = input("Enter student name: ")
            gradebook.calculate_average(name)

        elif choice == '6':
            gradebook.save_gradebook()
            print("Saving gradebook and exiting...")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
        
                