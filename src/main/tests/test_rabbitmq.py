from unittest.mock import patch
from src.main.core.rabbitmq import publish_order_created_message


@patch('main.core.rabbitmq.pika.BlockingConnection')
def test_publish_order_to_rabbitmq(mock_blocking_connection):
    order_data = {
        "order_id": 10,
        "item": "Laptop",
        "amount": 35000
    }

    # RabbitMQ publisher function
    publish_order_created_message(order_data)

    # RabbitMQ connection and channel
    mock_blocking_connection.assert_called_once()
    channel = mock_blocking_connection.return_value.channel.return_value
    channel.queue_declare.assert_called_once_with(queue='order_notifications_queue', durable=True)
    channel.basic_publish.assert_called_once()
