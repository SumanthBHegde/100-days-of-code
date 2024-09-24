#An Employee Management System

import csv
import os

class Employee:
    def __init__(self, name, age, department, salary):
        self.name = name
        self.age = age
        self.department = department
        self.salary = salary
        
    def to_dict(self):
        return{
            "name": self.name,
            "age": self.age,
            "department": self.department,
            "salary": self.salary
        }
        
class EmployeeManager:
    def __init__(self, filename):
        self.filename = filename
        self.employees = self.load_employees()
    
    def load_employees(self):
        employees = []
        if os.path.exists(self.filename):
            with open(self.filename, newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    employees.append(Employee(row['name'], int(row['age']), row['department'], float(row['salary'])))
        return employees
    
    def save_employees(self):
        with open(self.filename, mode='r', newline='') as f:
            writer = csv.DictReader(f, fieldnames=['name', 'age', 'department', 'salary'])
            writer.writeheader()
            for employee in self.employees:
                writer.writrow(employee.to_dict())
                
    def add_employee(self, name, age, department, salary):
        self.employees.append(Employee(name, age, department, salary))
        print(f"Employee {name} added successfully")
        
    def update_employee(self, name, age=None, department=None, salary=None):
        employee = self.find_employee(name)
        if employee:
            if age:
                employee.age = age
            if department:
                employee.department = department
            if salary:
                employee.salary = salary
            print(f"Employee {name}'s details updated.")
        else:
            print(f"Employee {name} not found")
    
    def remove_employee(self, name):
        employee = self.find_employee(name)
        if employee:
            self.employees.remove(employee)
            print(f"Employee {name} removed.")
        else:
            print(f"Employee {name} not found")
            
    def find_employee(self, name):
        for emp in self.employees:
            if emp.name == name:
                return emp
        return None
    
    def view_all_employees(self):
        if not self.employees:
            print(f"Employees not found")
            return
        print("------------------------------------------------")
        print("| Name          | Age  | Dept       | Salary   |")
        print("------------------------------------------------")
        for emp in self.employees:
            print(f"| {emp.name:<13} | {emp.age:<4} | {emp.department:<10} | {emp.salary:<8} |")
        print("------------------------------------------------")
    
    def calculate_average_salary(self, department=None):
        if not self.employees:
            print(f"No employees to calculate average salary")
            return
        
        # filtering by departments
        filtered_employees = [emp for emp in self.employees if department is None or emp.department == department]
        
        if not filtered_employees:
            print(f"No employees found in department: {department}" if department else "No employees found.")
            return
        total_salary = sum(emp.salary for emp in filtered_employees)
        avg_salary = total_salary / len(filtered_employees)
        
        if department:
            print(f"Average Salary in {department} Department: {avg_salary:.2f}")
        else:
            print(f"Average Salary for all employees: {avg_salary:.2f}")

def get_input(prompt, cast_type=str, optional=False):
    value = input(prompt)
    if optional and value == "":
        return None
    try:
        return cast_type(value)
    except ValueError:
        print(f"Invalid input. Expected {cast_type.__name__}.")
        return get_input(prompt, cast_type, optional)
    
def main():
    manager = EmployeeManager('employees.csv')

    actions = {
        '1': lambda: manager.add_employee(
            get_input("Enter employee name: "),
            get_input("Enter age: ", int),
            get_input("Enter department: "),
            get_input("Enter salary: ", float)
        ),
        '2': lambda: manager.update_employee(
            get_input("Enter employee name to update: "),
            get_input("Enter new age (or press Enter to skip): ", int, optional=True),
            get_input("Enter new department (or press Enter to skip): ", optional=True),
            get_input("Enter new salary (or press Enter to skip): ", float, optional=True)
        ),
        '3': lambda: manager.remove_employee(get_input("Enter employee name to remove: ")),
        '4': manager.view_all_employees,
        '5': lambda: manager.calculate_average_salary(get_input("Enter department (or press Enter for all): ", optional=True)),
        '6': lambda: manager.save_employees() or print("Saving employee records and exiting..."),
    }

    while True:
        print("\n1. Add Employee\n2. Update Employee\n3. Remove Employee\n4. View All Employees")
        print("5. Calculate Average Salary\n6. Save & Exit")
        
        choice = input("Choose an option: ").strip()

        action = actions.get(choice)
        if action:
            action()
            if choice == '6':
                break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()