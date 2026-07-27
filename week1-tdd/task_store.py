class Task():
    def __init__(self, description: str, completed: bool):
        self.description = description
        self.completed = completed
        self.id = None

class TaskStore():
    def __init__(self):
        self.tasks = []
        self.descriptions = set()
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
        return task.id

    def read_task(self, task_id: int):
        pass

    def update_task(self, task_id: int, description: str, completed: bool):
        pass

    def delete_task(self, task_id: int):
        pass