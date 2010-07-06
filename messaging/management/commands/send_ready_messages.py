from django.core.management.base import NoArgsCommand

from messaging.models import Queue

class Command(NoArgsCommand):
    Queue.objects.send_ready_messages()