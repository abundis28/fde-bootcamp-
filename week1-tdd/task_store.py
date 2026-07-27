class Task():
    def __init__(self, description: str, completed: bool):
        self.description = description
        self.completed = completed
        self.id = None

class TaskStore():
    def __init__(self):
        self.tasks = []
        self.descriptions = set()
        self.ids = set()
        self.next_id = 1

    def add_task(self, task: Task):
        if not isinstance(task.completed, bool):
            raise TypeError("Completed must be a boolean value.")
        if not isinstance(task.description, str):
            raise TypeError("Description must be a string.")
        if task.description in self.descriptions:
            raise ValueError("Task with this description already exists.")  
        task.id = self.next_id
        self.next_id += 1
        self.tasks.append(task)
        self.descriptions.add(task.description)
        self.ids.add(task.id)
        return task.id

    def read_task(self, task_id: int):
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id not in self.ids:
            raise KeyError("Task ID does not exist.")
        for task in self.tasks:
            if task.id == task_id:
                return task

    def update_task(self, task_id: int, description: str, completed: bool):
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if not isinstance(description, str):
            raise TypeError("Description must be a string.")
        if not isinstance(completed, bool):
            raise TypeError("Completed must be a boolean value.")
        if task_id not in self.ids:
            raise KeyError("Task ID does not exist.")
        if description in self.descriptions:
            raise ValueError("Task with this description already exists.")
        for task in self.tasks:
            if task.id == task_id:
                task.description = description
                task.completed = completed
                return True

    def delete_task(self, task_id: int):
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id not in self.ids:
            raise KeyError("Task ID does not exist.")
        for task in self.tasks:
            if task.id == task_id:
                self.tasks.remove(task)
                self.descriptions.remove(task.description)
                self.ids.remove(task.id)
                return True