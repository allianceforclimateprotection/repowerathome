from django.dispatch import Signal

logged_in = Signal(providing_args=["request", "user", "is_new_user"])