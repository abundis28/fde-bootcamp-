class Task():
    def __init__(self, description: str, completed: bool):
        self.description = description
        self.completed = completed

class TaskStore():
    def __init__(self):
        self.tasks = []

    def add_task(self, task: Task):
        pass

    def read_task(self, task_id: int):
        pass

    def update_task(self, task_id: int, description: str, completed: bool):
        pass

    def delete_task(self, task_id: int):
        pass