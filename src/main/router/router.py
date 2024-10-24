from fastapi import APIRouter
from src.main.core.rabbitmq import test_rabbitmq_connection

router = APIRouter()


# test channel connection RabbitMQ
@router.get("/test-rabbitmq")
def test_rabbitmq_route():
    test_rabbitmq_connection()
    return {"message": "Check console for RabbitMQ connection result"}
