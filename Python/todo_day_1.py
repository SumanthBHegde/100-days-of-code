#Todo app 

class Task:
    def __init__(self, description):
        self.description = description
        self.completed = False
        
    def mark_completed(self):
        self.completed = True
    
    def __str__(self):
        status = '[X]' if self.completed else '[]'
        return f"{status} {self.description}"
    

class ToDoList:
    def __init__(self):
        self.tasks = []
    
    def add_task(self, description):
        self.tasks.append(Task(description))
        
    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
    
    def mark_task_complete(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_completed()
            
    def view_tasks(self):
        for i, task in enumerate(self.tasks, start=1):
            print(f"\n{i}. {task}")
    
    def save_tasks(self, filename):
        with open(filename, 'w') as file:
            for task in self.tasks:
                file.write(f"{task.description},{task.completed}\n")
    
    def load_tasks(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    description, completed = line.strip().split(',')
                    task = Task(description)
                    if completed == 'True':
                        task.mark_completed()
                    self.tasks.append(task)
        except FileNotFoundError:
            pass
        

def main():
    todo_list = ToDoList()
    todo_list.load_tasks('tasks.txt')

    while True:
        print("\nChoose an option for operation : \n 1. Add Task\n 2. Remove Task\n 3. View Tasks\n 4. Mark Task as Complete\n 5. Save & Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            description = input("Enter task description: ")
            todo_list.add_task(description)
        elif choice == '2':
            index = int(input("Enter task number to remove: ")) - 1
            todo_list.remove_task(index)
        elif choice == '3':
            todo_list.view_tasks()
        elif choice == '4':
            index = int(input("Enter task number to mark as complete: ")) - 1
            todo_list.mark_task_complete(index)
            todo_list.view_tasks()
        elif choice == '5':
            todo_list.save_tasks('tasks.txt')
            print("Tasks saved to file. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()