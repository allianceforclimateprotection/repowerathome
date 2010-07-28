from django.dispatch import Signal

record_created = Signal(providing_args=["request", "record"])