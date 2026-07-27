import pytest
from task_store import TaskStore, Task

def test_add_task():
    # Arrange
    task_store = TaskStore()
    task = Task("Get bread", False)
    # Act
    task_id = task_store.add_task(task)
    # Assert
    assert task_id is not None

def test_add_task_incorrect_type():
    # Arrange
    task_store = TaskStore()
    task = Task("Get bread", 12)
    # Act & Assert
    with pytest.raises(TypeError):
        task_store.add_task(task)

def test_read_task_id_exists():
    # Arrange
    task_store = TaskStore()
    task = Task("Get bread", False)
    task_id = task_store.add_task(task)
    # Act
    retrieved_task = task_store.read_task(task_id)
    # Assert
    assert retrieved_task is not None
    assert retrieved_task.description == "Get bread"
    assert retrieved_task.completed == False

def test_read_task_id_does_not_exist():
    # Arrange
    task_store = TaskStore()
    # Act & Assert
    with pytest.raises(KeyError):
        task_store.read_task(999)

def test_read_task_incorrect_type():
    # Arrange
    task_store = TaskStore()
    # Act & Assert
    with pytest.raises(TypeError):
        task_store.read_task("invalid_id")

def test_update_task_id_exists():
    # Arrange
    task_store = TaskStore()
    task = Task("Get bread", False)
    task_id = task_store.add_task(task)
    # Act
    task_update_status = task_store.update_task(task_id, "Get Milk", False)
    # Assert
    assert task_update_status is True
    assert task_store.read_task(task_id).description == "Get Milk"
    assert task_store.read_task(task_id).completed == False

def test_update_task_id_does_not_exist():
    # Arrange
    task_store = TaskStore()
    # Act & Assert
    with pytest.raises(KeyError):
        task_store.update_task(999, "Get Milk", False)

def test_update_task_incorrect_type():
    # Arrange
    task_store = TaskStore()
    task = Task("Get bread", False)
    task_id = task_store.add_task(task)
    # Act & Assert
    with pytest.raises(TypeError):
        task_store.update_task(task_id, 123, False)

def test_delete_task_id_exists():
    # Arrange
    task_store = TaskStore()
    task = Task("Get bread", False)
    task_id = task_store.add_task(task)
    # Act & Assert
    assert task_store.delete_task(task_id) == True

def test_delete_task_id_does_not_exist():
    # Arrange
    task_store = TaskStore()
    # Act & Assert
    with pytest.raises(KeyError):
        task_store.delete_task(999)