import random

class Task():
    def __init__(self, description: str, completed: bool):
        self.description = description
        self.completed = completed
        self.id = None

class TaskStore():
    def __init__(self, id_generator=None):
        self.tasks = {}
        self.next_id = 1
        self.id_generator = id_generator or self._default_id_generator

    def _default_id_generator(self):
        task_id = self.next_id
        self.next_id += 1
        return task_id

    def add_task(self, task: Task):
        if not isinstance(task.completed, bool):
            raise TypeError("Completed must be a boolean value.")
        if not isinstance(task.description, str):
            raise TypeError("Description must be a string.")
        task.id = self.id_generator()
        self.tasks[task.id] = task
        return task.id

    def read_task(self, task_id: int):
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id not in self.tasks:
            raise KeyError("Task ID does not exist.")
        return self.tasks.get(task_id)

    def update_task(self, task_id: int, **changes):
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if not isinstance(changes.get("description"), str):
            raise TypeError("Description must be a string.")
        if not isinstance(changes.get("completed"), bool):
            raise TypeError("Completed must be a boolean value.")
        if task_id not in self.tasks:
            raise KeyError("Task ID does not exist.")
        task = self.tasks[task_id]
        task.description = changes.get("description")
        task.completed = changes.get("completed")
        return True

    def delete_task(self, task_id: int):
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id not in self.tasks:
            raise KeyError("Task ID does not exist.")
        self.tasks.pop(task_id)
        return True