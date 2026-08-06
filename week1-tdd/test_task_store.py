import pytest
from task_store import TaskStore, Task

@pytest.fixture
def task_store():
    return TaskStore()

@pytest.fixture
def store_with_task(task_store):
    task = Task("Get bread", False)
    task_id = task_store.add_task(task)
    return task_store, task_id

def test_add_task(task_store):
    # Arrange
    task = Task("Get bread", False)
    # Act
    task_id = task_store.add_task(task)
    # Assert
    assert task_id is not None

@pytest.mark.parametrize("description, completed", [
    (123, False),          # bad description
    ("Get bread", 12),     # bad completed
    (None, False),         # bad description
    ("Get bread", None)    # bad completed
])
def test_add_task_incorrect_types(task_store, description, completed):
    # Arrange
    task_store = TaskStore()
    # Act & Assert
    with pytest.raises(TypeError):
        task_store.add_task(Task(description, completed))

def test_read_task_id_exists(store_with_task):
    # Arrange
    task_store, task_id = store_with_task
    # Act
    retrieved_task = task_store.read_task(task_id)
    # Assert
    assert retrieved_task is not None
    assert retrieved_task.description == "Get bread"
    assert retrieved_task.completed == False

def test_read_task_id_does_not_exist(task_store):
    # Arrange
    # Act & Assert
    with pytest.raises(KeyError):
        task_store.read_task(999)

@pytest.mark.parametrize("p_id", [
    ("invalid_id"),        # bad id
    (""),                  # empty string
    (None)                 # None value
])
def test_read_task_incorrect_type(task_store, p_id):
    # Arrange
    # Act & Assert
    with pytest.raises(TypeError):
        task_store.read_task(p_id)

def test_update_task_id_exists(store_with_task):
    # Arrange
    task_store, task_id = store_with_task
    # Act
    task_update_status = task_store.update_task(task_id, description="Get Milk", completed=False)
    # Assert
    assert task_update_status is True
    assert task_store.read_task(task_id).description == "Get Milk"
    assert task_store.read_task(task_id).completed == False

def test_update_task_id_does_not_exist(task_store):
    # Arrange
    # Act & Assert
    with pytest.raises(KeyError):
        task_store.update_task(999, description="Get Milk", completed=False)

@pytest.mark.parametrize("id, description, completed", [
    (123, "Get Milk", False),          # bad description
    (456, "Get bread", 12),     # bad completed
    (789, None, False) ,         # bad description
    (0, "Get bread", None),    # bad completed
    ("invalid_id", "Get Milk", False),        # bad id
    ("", "Get bread", 12),                  # empty string
    (None, "Get bread", None)                 # None value
])
def test_update_task_incorrect_type(store_with_task, id, description, completed):
    # Arrange
    task_store, _ = store_with_task
    # Act & Assert
    with pytest.raises(TypeError):
        task_store.update_task(id, description, completed)

def test_delete_task_id_exists(store_with_task):
    # Arrange
    task_store, task_id = store_with_task
    # Act & Assert
    assert task_store.delete_task(task_id) == True

def test_delete_task_id_does_not_exist(task_store):
    # Arrange
    # Act & Assert
    with pytest.raises(KeyError):
        task_store.delete_task(999)

@pytest.mark.parametrize("p_id", [
    ("invalid_id"),        # bad id
    (""),                  # empty string
    (None)                 # None value
])
def test_delete_task_incorrect_type(task_store, p_id):
    # Arrange
    # Act & Assert
    with pytest.raises(TypeError):
        task_store.delete_task(p_id)