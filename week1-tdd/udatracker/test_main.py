from xmlrpc import client

from fastapi.testclient import TestClient
import pytest
from main import app

@pytest.fixture
def client_with_orders():
    app.state.orders = {
        1: {"order_id": 1, "customer_name": "John Doe", "items": [], "status": "shipped", "total_amount": 100.0, "created_at": "2023-01-01T00:00:00"},
        2: {"order_id": 2, "customer_name": "Jane Smith", "items": [], "status": "processing", "total_amount": 200.0, "created_at": "2023-01-02T00:00:00"},
        3: {"order_id": 3, "customer_name": "Bob Johnson", "items": [], "status": "delivered", "total_amount": 300.0, "created_at": "2023-01-03T00:00:00"},
    }
    with TestClient(app) as client:
        yield client
    app.state.orders = {}  # Clean up after the test

@pytest.fixture
def client_without_orders():
    return TestClient(app)

@pytest.mark.parametrize("order_id, status", [
    (1, "shipped"),
    (2, "processing"),
    (3, "delivered")
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

@pytest.mark.parametrize("order_id", ["invalid_id", "", None])
def test_uda_get_orders_incorrect_type(client_with_orders, order_id):
    # Arrange
    # Act
    response = client_with_orders.get(f"/orders/{order_id}")
    # Assert
    # Empty path segment becomes "/orders/" which does not match the route (404).
    if order_id == "":
        assert response.status_code == 404
    else:
        assert response.status_code == 422  # Unprocessable Entity for invalid types