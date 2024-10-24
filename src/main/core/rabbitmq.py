
import pika
import json
import traceback

from src.main.config import get_settings, Settings
settings: Settings = get_settings()


def get_rabbitmq_channel():
    """Connect to RabbitMQ and return a channel."""
    connection_params = pika.URLParameters(settings.RABBITMQ_URL)
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue='order_notifications_queue', durable=True)

    return channel


# Test connection function
def test_rabbitmq_connection():
    try:
        channel = get_rabbitmq_channel()
        print("RabbitMQ connection established successfully!")
        channel.close()

    except pika.exceptions.AMQPConnectionError as e:
        print(f"Failed to connect to RabbitMQ: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()


# Function to publish a message to the RabbitMQ queue
def publish_order_created_message(order_data: dict):
    """Publish an 'order created' message to RabbitMQ."""
    channel = get_rabbitmq_channel()

    # convert order data to a dict
    message = json.dumps(order_data).encode('utf-8')

    # Publish the message to the queue
    channel.basic_publish(
        exchange='',
        routing_key='order_notifications_queue',  # Name of the queue
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,
        )
    )
    print(f"Published message to RabbitMQ: {message}")
    channel.close()


