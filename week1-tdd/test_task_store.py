import pytest
from task_store import TaskStore, Task
from unittest.mock import Mock

@pytest.fixture
def task_store():
    id_generator = Mock(return_value=1)
    return TaskStore(id_generator=id_generator)

@pytest.fixture
def store_with_task(task_store):
    task = Task("Get bread", False)
    task_id = task_store.add_task(task)
    return task_store, task_id

@pytest.fixture
def store_with_no_id_mock():
    return TaskStore(id_generator=None)

def test_add_task_with_no_id_generator(store_with_no_id_mock):
    # Arrange
    task = Task("Get bread", False)
    # Act
    task_id = store_with_no_id_mock.add_task(task)
    # Assert
    assert task_id is not None

def test_add_multiple_tasks_with_no_id_generator(store_with_no_id_mock):
    # Arrange
    task1 = Task("Get bread", False)
    task2 = Task("Get milk", True)
    # Act
    task_id1 = store_with_no_id_mock.add_task(task1)
    task_id2 = store_with_no_id_mock.add_task(task2)
    # Assert
    assert task_id1 is not None
    assert task_id2 is not None
    assert task_id1 != task_id2

def test_add_uses_injected_id_generator():
    gen = Mock(return_value=42)
    store = TaskStore(id_generator=gen)
    task_id = store.add_task(Task("Get bread", False))
    assert task_id == 42
    gen.assert_called_once()

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

@pytest.mark.parametrize("description, completed", [
    (12, False),          # bad description
    ("Get bread", 12),     # bad completed
    (None, False) ,         # bad description
    ("Get bread", None),    # bad completed
])
def test_update_task_incorrect_type(store_with_task, description, completed):
    # Arrange
    task_store, id = store_with_task
    # Act & Assert
    with pytest.raises(TypeError):
        task_store.update_task(id, description=description, completed=completed)

@pytest.mark.parametrize("p_id", [
    ("invalid_id"),        # bad id
    (""),                  # empty string
    (None)                 # None value
])
def test_update_task_incorrect_id_type(task_store, p_id):
    # Arrange
    # Act & Assert
    with pytest.raises(TypeError):
        task_store.update_task(p_id, description="Get Milk", completed=False)

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