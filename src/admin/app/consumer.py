# src/admin/app/consumers.py

import pika
import africastalking
import json
import logging
from django.conf import settings

# Initialize Africa's Talking API
africastalking.initialize(
    username=settings.AFRICASTALKING_USERNAME,
    api_key=settings.AFRICASTALKING_API_KEY
)

sms = africastalking.SMS
log = logging.getLogger(__name__)


# Function to send SMS using Africa's Talking
def send_sms(phone_number, message):

    try:
        response = sms.send(message, [phone_number], sender="TC4A")
        log.info(f"SMS sent to {phone_number}: {response}")
    except Exception as e:
        log.error(f"Failed to send SMS: {e}")


# RabbitMQ callback function
def process_order(ch, method, properties, body):
    """Callback function for processing order messages from RabbitMQ."""
    try:
        order_data = json.loads(body)
        log.info(f"Received order: {order_data}")

        # Prepare the SMS message
        message = f"Hello! Your order for {order_data['item']} worth {order_data['amount']} has been placed successfully."

        # Send SMS to the customer
        send_sms(order_data["+254723262333"], message)

        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        log.error(f"Error processing order: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)


# Function to start consuming messages from RabbitMQ
def start_rabbitmq_consumer():
    """Connect to RabbitMQ and start consuming messages."""
    connection_params = pika.URLParameters(settings.RABBITMQ_URL)
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.queue_declare(queue='order_notifications_queue', durable=True)

    # Start consuming messages from the queue
    channel.basic_consume(
        queue='order_notifications_queue',
        on_message_callback=process_order
    )

    log.info("Started consuming messages from RabbitMQ")
    channel.start_consuming()
