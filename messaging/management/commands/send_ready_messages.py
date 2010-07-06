from django.core.management.base import BaseCommand

from messaging.models import Queue

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        Queue.objects.send_ready_messages()