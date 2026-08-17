from fastapi.testclient import TestClient
import pytest
from main import app

@pytest.fixture(autouse=True)
def client_restore():
    app.state.orders.clear()
    app.state.next_order_id = 1
    yield

@pytest.fixture
def client_with_orders():
    app.state.orders = {
        1: {"order_id": 1, "customer_name": "John Doe", "items": [], "status": "shipped", "total_amount": 100.0, "created_at": "2023-01-01T00:00:00"},
        2: {"order_id": 2, "customer_name": "Jane Smith", "items": [], "status": "pending", "total_amount": 200.0, "created_at": "2023-01-02T00:00:00"},
        3: {"order_id": 3, "customer_name": "Bob Johnson", "items": [], "status": "paid", "total_amount": 300.0, "created_at": "2023-01-03T00:00:00"},
    }
    with TestClient(app) as client:
        yield client

@pytest.fixture
def client_without_orders():
    app.state.orders = {}
    app.state.next_order_id = 1
    with TestClient(app) as client:
        yield client

@pytest.mark.parametrize("order_id, status", [
    (1, "shipped"),
    (2, "pending"),
    (3, "paid")
])
def test_uda_get_orders_id_exists(client_with_orders, order_id, status):
    # Arrange
    # Act
    response = client_with_orders.get(f"/orders/{order_id}")
    # Assert
    assert response.status_code == 200
    assert response.json()["order_id"] == order_id
    assert response.json()["status"] == status

@pytest.mark.parametrize("order_id, status", [
    (999, "Order not found"),
    (1000, "Order not found"),
    (1001, "Order not found")
])
def test_uda_get_orders_id_does_not_exist(client_with_orders, order_id, status):
    # Arrange
    # Act
    response = client_with_orders.get(f"/orders/{order_id}")
    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": status}

@pytest.mark.parametrize("order_id", ["invalid_id", None])
def test_uda_get_orders_incorrect_type(client_with_orders, order_id):
    # Arrange
    # Act
    response = client_with_orders.get(f"/orders/{order_id}")
    # Assert
    # Empty path segment becomes "/orders/" which does not match the route (404).
    if order_id == "":
        assert response.status_code == 405
    else:
        assert response.status_code == 422  # Unprocessable Entity for invalid types

@pytest.mark.parametrize("customer_name, items, total_amount", [
    ("John Doe", [{"product_id": "item1", "quantity": 2, "unit_price": 10.0}], 20.0),
    ("Jane Smith", [{"product_id": "item3", "quantity": 3, "unit_price": 15.0}, {"product_id": "item4", "quantity": 2, "unit_price": 25.0}], 95.0),
    ("Bob Johnson", [{"product_id": "item5", "quantity": 1, "unit_price": 30.0}, {"product_id": "item6", "quantity": 2, "unit_price": 35.0}, {"product_id": "item7", "quantity": 1, "unit_price": 40.0}], 140.0)
])
def test_uda_post_order(client_without_orders, customer_name, items, total_amount):
    # Arrange
    # Act
    response = client_without_orders.post("/orders", json={"customer_name": customer_name, "items": items})
    # Assert
    assert response.status_code == 201
    assert response.json()["order_id"] is not None
    assert response.json()["customer_name"] == customer_name
    assert response.json()["items"] == items
    assert response.json()["status"] == "pending"
    assert response.json()["total_amount"] == total_amount
    assert response.json()["created_at"] is not None

@pytest.mark.parametrize("customer_name, items, total_amount", [
    ("", [{"product_id": "item1", "quantity": 2, "unit_price": 10.0}], 20.0),  # Empty customer name
    ("John Doe", [], 0.0),  # Empty items list
    ("Jane Smith", [{"product_id": "item2", "quantity": 1, "unit_price": -5.0}], -5.0),  # Negative unit price
    ("Bob Johnson", [{"product_id": "item3", "quantity": 0, "unit_price": 10.0}], 0.0)  # Zero quantity
])
def test_uda_post_order_invalid_data(client_without_orders, customer_name, items, total_amount):
    # Arrange
    # Act
    response = client_without_orders.post("/orders", json={"customer_name": customer_name, "items": items})
    # Assert
    assert response.status_code == 422  # Unprocessable Entity for invalid data

def test_uda_post_order_extra_fields(client_without_orders):
    # Arrange
    extra_data = {
        "customer_name": "John Doe",
        "items": [{"product_id": "item1", "quantity": 2, "unit_price": 10.0}],
        "total_amount": 0.0,  # This field should be calculated, not provided
        "order_id": 999,  # This field should be generated, not provided
        "status": "paid",  # This field should be set to "pending" initially
    }
    # Act
    response = client_without_orders.post("/orders", json=extra_data)
    # Assert
    assert response.status_code == 201  # Created for valid order with extra fields
    assert response.json()["order_id"] != 999  # The order_id should be generated, not taken from the request
    assert response.json()["status"] == "pending"  # The status should be set to "pending"
    assert response.json()["total_amount"] == 20.0  # The total_amount should be calculated based on items

def test_uda_post_order_free(client_without_orders):
    # Arrange
    free_order_data = {
        "customer_name": "Free Customer",
        "items": [{"product_id": "item_free", "quantity": 1, "unit_price": 0.0}],
    }
    # Act
    response = client_without_orders.post("/orders", json=free_order_data)
    # Assert
    assert response.status_code == 201  # Created for valid order with free item
    assert response.json()["total_amount"] == 0.0  # The total_amount should be zero for free items

def test_uda_patch_existingId_validStatus_hp(client_with_orders):
    #Arrange
    update_payload = {
        "status": "shipped"
    }
    order_id = 2  # Existing order ID
    #Act
    response = client_with_orders.patch(f"/orders/{order_id}", json=update_payload)
    #Assert
    assert response.status_code == 200
    assert response.json()["order_id"] == order_id
    assert response.json()["status"] == "shipped"

@pytest.mark.parametrize("order_id, json_status", [
    (1, "purchased"),
    (2, ""),
    (3, 5)
])
def test_uda_patch_existingId_invalidStatus(client_with_orders, order_id, json_status):
    #Arrange
    #Act
    response = client_with_orders.patch(f"/orders/{order_id}", json=json_status)
    #Assert
    assert response.status_code == 422

def test_uda_patch_nonExistingId(client_with_orders):
    #Arrange
    update_payload = {
        "status": "shipped"
    }
    order_id = 999  # Non-existing order ID
    #Act
    response = client_with_orders.patch(f"/orders/{order_id}", json=update_payload)
    #Assert
    assert response.status_code == 404

@pytest.mark.parametrize("order_id", [
    ("invalid_id"),        # bad id
    (None)                 # None value
])
def test_uda_patch_invalidId(client_with_orders, order_id):
    #Arrange
    update_payload = {
        "status": "shipped"
    }
    #Act
    response = client_with_orders.patch(f"/orders/{order_id}", json=update_payload)
    #Assert
    assert response.status_code == 422

def test_uda_patch_missingStatus(client_with_orders):
    #Arrange
    update_payload = {
        # Missing "status" field
    }
    order_id = 1  # Existing order ID
    #Act
    response = client_with_orders.patch(f"/orders/{order_id}", json=update_payload)
    #Assert
    assert response.status_code == 422

@pytest.mark.parametrize("order_id, status", [
    (1, "shipped"),
    (1, "pending"),
    (1, "paid")
])
def test_uda_patch_invalidTransition_br(order_id, status):
    #Arrange
    update_payload = {
        "status": status  # Invalid type for status
    }
    order_id = order_id  # Existing order ID
    app.state.orders = {
        1: {"order_id": 1, "customer_name": "John Doe", "items": [], "status": "cancelled", "total_amount": 100.0, "created_at": "2023-01-01T00:00:00"},
    }
    #Act
    with TestClient(app) as client:
        response = client.patch(f"/orders/{order_id}", json=update_payload)
    #Assert
    assert response.status_code == 409

def test_uda_get_query_orders_by_status(client_with_orders):
    # Arrange
    status = "pending"
    # Act
    response = client_with_orders.get(f"/orders?status={status}")
    # Assert
    assert response.status_code == 200
    orders = response.json()
    assert all(order["status"] == status for order in orders)

@pytest.mark.parametrize("status", [
    "purchased",
    "",
    4
])
def test_uda_get_query_invalid_status(client_with_orders, status):
    #Arrange
    #Act
    response = client_with_orders.get(f"/orders?status={status}")
    #Assert
    assert response.status_code == 422

def test_uda_get_query_no_orders(client_without_orders):
    # Arrange
    status = "cancelled"
    # Act
    response = client_without_orders.get(f"/orders?status={status}")
    # Assert
    assert response.status_code == 200
    orders = response.json()
    assert orders == []  # Should return an empty list when no orders exist

def test_uda_get_query_no_status(client_with_orders):
    # Arrange
    # Act
    response = client_with_orders.get("/orders")
    # Assert
    assert response.status_code == 200
    orders = response.json()
    assert len(orders) == 3  # Should return all orders when no status is provided

@pytest.mark.parametrize("order_id", [1, 2, 3])
def test_uda_delete_existingId(client_with_orders, order_id):
    #Arrange
    #Act
    delete_response = client_with_orders.delete(f"/orders/{order_id}")
    #Assert
    assert delete_response.status_code == 200
    assert app.state.orders[order_id]["status"] == "cancelled"

def test_uda_delete_nonExistingId(client_with_orders):
    #Arrange
    order_id = 999
    #Act
    response = client_with_orders.delete(f"/orders/{order_id}")
    #Assert
    assert response.status_code == 404

def test_uda_delete_alreadyCancelled(client_with_orders):
    #Arrange
    order_id = 1  # Existing order ID
    # First, cancel the order
    client_with_orders.delete(f"/orders/{order_id}")
    #Act
    response = client_with_orders.delete(f"/orders/{order_id}")
    #Assert
    assert response.status_code == 200

@pytest.mark.parametrize("order_id", ["id", None, 0, -1])
def test_uda_delete_invalidID(client_with_orders, order_id):
    #Arrange
    #Act
    response = client_with_orders.delete(f"/orders/{order_id}")
    #Assert
    assert response.status_code == 422
