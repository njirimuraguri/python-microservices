import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.main.main import app

client = TestClient(app)

# Sample order data
sample_order = {
    "item": "Laptop",
    "amount": 1500,
    "customer_phone": "+25723262333"
}


# Test order creation
def test_create_order():
    # Mock the RabbitMQ publishing function
    with patch('main.core.rabbitmq.publish_order_created_message') as mock_publish:
        response = client.post("/orders/", json=sample_order)

        # Check that the API responds with a successful creation
        assert response.status_code == 201
        data = response.json()
        assert data["item"] == sample_order["item"]
        assert data["amount"] == sample_order["amount"]
        assert data["customer_phone"] == sample_order["customer_phone"]

        mock_publish.assert_called_once_with({
            "order_id": data["id"],
            "phone_number": data["customer_phone"]
            "item": data["item"],
            "amount": data["amount"]
        })


# Test fetching order by ID
def test_get_order():
    response = client.post("/orders/", json=sample_order)
    assert response.status_code == 201
    created_order = response.json()

    # Fetch the order by its ID
    order_id = created_order["id"]
    response = client.get(f"/orders/{order_id}")

    # Check that the API responds with the correct order data
    assert response.status_code == 200
    fetched_order = response.json()
    assert fetched_order["item"] == sample_order["item"]
    assert fetched_order["amount"] == sample_order["amount"]
    assert fetched_order["customer_phone"] == sample_order["customer_phone"]


# Test fetching all orders (with pagination)
def test_get_all_orders():
    response = client.get("/orders/")
    assert response.status_code == 200
    data = response.json()

    # Check if orders list is returned
    assert isinstance(data, list)
    assert len(data) > 0


# Test deleting an order
def test_delete_order():
    response = client.post("/orders/", json=sample_order)
    assert response.status_code == 201
    created_order = response.json()

    # Delete the order by its ID
    order_id = created_order["id"]
    delete_response = client.delete(f"/orders/{order_id}")

    # Check that the deletion was successful
    assert delete_response.status_code == 200

    # Ensure the order no longer exists
    get_response = client.get(f"/orders/{order_id}")
    assert get_response.status_code == 404
