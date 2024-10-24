# Python Microservices Project

A microservices-based backend system using FastAPI and Django to manage customers and orders. The project demonstrates the use of **Docker** for containerization, **RabbitMQ** for event handling, **PostgreSQL** for data storage, and **OAuth2** for authentication.

---

## Tech Stack

- **FastAPI**: Main API service for managing customers and orders.
- **Django**: Admin service to manage internal operations and sending SMS notifications.
- **RabbitMQ**: Message broker for event-driven communication between services.
- **PostgreSQL**: Database used for storing customers, orders, and user data.
- **Docker**: Used for containerizing the services.
- **OAuth2 with JWT**: Used for authentication.
- **Alembic**: For handling database migrations in the FastAPI service.
- **Africa’s Talking SMS API**: Integration to send SMS notifications when an order is placed.

---

## Project Structure

```
python-microservices/
├── alembic/                     
│   ├── versions/
│       ├── __init__.py
│       ├── env.py
│       ├── README
│       └── script.py.mako
├── db/                           # PostgreSQL Docker configuration
│   └── Dockerfile
├── migrations/                  
│   ├── versions/
│       ├── __init__.py
│       ├── env.py
│       ├── README
│       └── script.py.mako
├── src/
│   ├── admin/                    # Django Admin Service
│   │   ├── __init__.py      
│   │   ├── Dockerfile           # Dockerfile for Django service
│   │   ├── manage.py             # Entry point for Django
│   │   ├── admin/                # Django project folder
│   │   │   ├── __init__.py 
│   │   │   ├── settings.py       # Django settings
│   │   │   ├── asgi.py           # ASGI config
│   │   │   ├── urls.py           # URL routing for Django
│   │   │   ├── wsgi.py           # WSGI config
│   │   └── app/                  # Django apps folder
│   │       ├── migrations/     
│   │       ├── __init__.py
│   │       ├── admin.py
│   │       ├── apps.py
│   │       ├── models.py
│   │       ├── views.py
│   │       ├── urls.py
│   │       └── tests.py          # Unit tests for Django service
│   ├── main/                     # FastAPI Service
│   │   ├── __init__.py           # Marking main as a package
│   │   ├── alembic/              # Alembic database migrations
│   │   │   └── versions/
│   │   ├── auth/                 # Authentication and Authorization
│   │   │   ├── __init__.py
│   │   │   ├── jwt_security.py
│   │   │   └── schemas.py
│   │   ├── core/                 # Core configurations (RabbitMQ, dependencies)
│   │   │   ├── __init__.py
│   │   │   └── dependencies.py
│   │   ├── customer/             # Customer module
│   │   │   ├── __init__.py
│   │   │   ├── crud.py           # Customer CRUD operations
│   │   │   ├── model.py          # Customer model
│   │   │   └── schema.py         # Pydantic schemas for customer
│   │   ├── database/             # Database configuration
│   │   │   ├── __init__.py
│   │   │   ├── base.py           # Base models
│   │   │   └── session.py        # Database session management
│   │   ├── orders/               # Orders module
│   │   │   ├── __init__.py
│   │   │   ├── crud.py           # Order CRUD operations
│   │   │   ├── model.py          # Order model
│   │   │   └── schema.py         # Pydantic schemas for order
│   │   ├── router/               # FastAPI Router
│   │   │   ├── __init__.py
│   │   │   ├── routes.py         # API routes for FastAPI
│   │   ├── Dockerfile            # Dockerfile for FastAPI service
│   │   └── main.py               # FastAPI entry point
├── venv/                         # Python virtual environment
├── .env                          # Environment variables
├── .gitignore               
├── alembic.ini               
├── docker-compose.yml            # Docker Compose configuration
├── README.md                     # Project README
├── requirements.txt              # Project dependencies
├── requirements-dev.txt          # Development dependencies

```

---

## Setup and Run the Project

### Prerequisites
- Install **Docker** and **Docker Compose** on your system. You can follow the official installation instructions [here](https://docs.docker.com/get-docker/).

### Steps to Run the Project

1. **Clone the repository**:
   ```bash
   git clone https://github.com/njirimuraguri@gmail.com/python-microservices.git
   ```

2. **Create `.env` file**:
   Inside the root of the project, create a `.env` file with the following content:

   ```env
   # Postgres
   POSTGRES_USER=****
   POSTGRES_PASSWORD=****
   POSTGRES_DB=****
   POSTGRES_SERVER=****

   # RabbitMQ
   RABBITMQ_DEFAULT_USER=guest
   RABBITMQ_DEFAULT_PASS=guest
   RABBITMQ_URL= your url from cloudAMQP

   # Africa’s Talking SMS API
   USERNAME=sandbox
   API_KEY=your api_key
   ```

3. **Build and run the Docker containers**:
   ```bash
   docker-compose up -d --build
   ```

4. **Access the services**:
   - **FastAPI (Main Service)**: http://localhost:8001
   - **Django Admin Service**: http://localhost:8000
   - **RabbitMQ Management**: http://localhost:15672 (Login with `guest` as username and password)

---

## API Endpoints

### **FastAPI Endpoints (Main Service)**

| Method  | Endpoint                              | Description                        |
|---------|---------------------------------------|------------------------------------|
| POST    | `/auth/register`                      | Register a new user                |
| POST    | `/auth/token`                         | Obtain JWT access token            |
| GET     | `/users/me`                           | Get the authenticated user         |
| POST    | `/customer/`                          | Create a customer                  |
| GET     | `/customer/`                          | Get all customers                  |
| GET     | `/customer/{customer_id}`             | Get customer by ID                 |
| PUT     | `/customer/{customer_id}`             | Update customer by ID              |
| DELETE  | `/customer/{customer_id}`             | Delete customer by ID              |
| POST    | `/orders/`                            | Create an order                    |
| GET     | `/orders/`                            | Get all orders                     |
| GET     | `/orders/{order_id}`                  | Get order by ID                    |
| PUT     | `/orders/{order_id}`                  | Update order by ID                 |
| DELETE  | `/orders/{order_id}`                  | Delete order by ID                 |

**API Routes:**

- **Auth & Customer API Endpoints:**
  ![111](https://github.com/user-attachments/assets/14b9ef80-53e5-49a2-96aa-3c7faeceecb5)


- **Order API Endpoints:**

![2222](https://github.com/user-attachments/assets/e1fe0552-143e-42d4-89d6-90b97dd48b70)


---

## Running Tests

1. **Run Unit Tests** (inside the FastAPI or Django containers):
   ```bash
   docker-compose exec fastapi-main pytest --cov=src/main
   docker-compose exec django-admin pytest --cov=src/admin
   ```

2. **Generate Coverage Reports**:
   ```bash
   pytest --cov=src/main --cov-report term-missing
   ```

---

## Project Containers

The services running in Docker include:
1. **FastAPI Service** (`fastapi-main`)
2. **Django Admin Service** (`django-admin`)
3. **RabbitMQ** (with management UI at port `15672`)
4. **PostgreSQL** (running at port `5432`)

**Containers Overview Screenshot:**

![containers](https://github.com/user-attachments/assets/76afb74a-5823-419f-aeea-ee7268d03541)

---

## License

This project is licensed under the MIT License.

---
