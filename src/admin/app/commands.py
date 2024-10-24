from django.core.management.base import BaseCommand
from src.admin.app.consumer import start_rabbitmq_consumer


class Command(BaseCommand):
    help = 'Run RabbitMQ consumer to listen for order notifications'

    def handle(self, *args, **kwargs):
        start_rabbitmq_consumer()
