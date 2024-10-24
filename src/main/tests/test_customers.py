import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.main.main import app

client = TestClient(app)

# Sample customer data
sample_customer = {
    "name": "njiri muraguri",
    "country": "Kenya",
    "email": "njirimuraguri@gmail.com",
    "phone_number": "+254723262333",
    "gender": "male",
    "password": "qwerty"
}

# Sample data for updating a customer
updated_customer_data = {
    "name": "njiri muraguri",
    "country": "Kenya",
    "email": "njirimuraguri@gmail.com",
    "phone_number": "+254723262333",
    "gender": "male",
}


# Test creating a customer
def test_create_customer():
    # Mock the RabbitMQ function to ensure RabbitMQ is not actually hit
    with patch('main.core.rabbitmq.publish_order_created_message') as mock_publish:
        response = client.post("/customers/", json=sample_customer)

        # Assert successful creation
        assert response.status_code == 201
        created_customer = response.json()
        assert created_customer["name"] == sample_customer["name"]
        assert created_customer["email"] == sample_customer["email"]
        assert created_customer["phone_number"] == sample_customer["phone_number"]

        # RabbitMQ mock should not be triggered here since it's not related to customer creation
        mock_publish.assert_not_called()


# Test fetching a customer by ID
def test_get_customer_by_id():
    # First, create the customer
    response = client.post("/customers/", json=sample_customer)
    assert response.status_code == 201
    created_customer = response.json()

    # Fetch the customer by ID
    customer_id = created_customer["id"]
    response = client.get(f"/customers/{customer_id}")

    # Assert successful retrieval
    assert response.status_code == 200
    fetched_customer = response.json()
    assert fetched_customer["name"] == sample_customer["name"]
    assert fetched_customer["email"] == sample_customer["email"]


# Test fetching all customers
def test_get_all_customers():
    response = client.get("/customers/")
    assert response.status_code == 200
    customers = response.json()

    # Ensure a list of customers is returned
    assert isinstance(customers, list)
    assert len(customers) > 0  # Ensure that there's at least one customer


# Test updating a customer
def test_update_customer():
    # First, create a customer
    response = client.post("/customers/", json=sample_customer)
    assert response.status_code == 201
    created_customer = response.json()

    # Update the customer data
    customer_id = created_customer["id"]
    response = client.put(f"/customers/{customer_id}", json=updated_customer_data)

    # Assert successful update
    assert response.status_code == 200
    updated_customer = response.json()
    assert updated_customer["name"] == updated_customer_data["name"]
    assert updated_customer["email"] == updated_customer_data["email"]
    assert updated_customer["phone_number"] == updated_customer_data["phone_number"]


# Test deleting a customer
def test_delete_customer():
    # First, create a customer
    response = client.post("/customers/", json=sample_customer)
    assert response.status_code == 201
    created_customer = response.json()

    # Delete the customer by ID
    customer_id = created_customer["id"]
    response = client.delete(f"/customers/{customer_id}")

    # Assert successful deletion
    assert response.status_code == 200

    # Ensure the customer no longer exists
    response = client.get(f"/customers/{customer_id}")
    assert response.status_code == 404
