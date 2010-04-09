from django.db.models import get_models, signals
from django.contrib.auth import models as auth_app

def create_default_users(app, created_models, verbosity, **kwargs):
    from django.contrib.auth.models import User
    from django.core.management import call_command
    if User in created_models and kwargs.get('interactive', True):
        msg = "\nYou just installed Django's auth system, woudl you like to install the " \
                "standard set of RAH users? (yes/no): "
        confirm = raw_input(msg)
        while 1:
            if confirm not in ('yes', 'no'):
                confirm = raw_input('Please enter either "yes" or "no": ')
                continue
            if confirm == 'yes':
                call_command("loaddata", "fixtures/auth.json", verbosity=0, interactive=True)
            break

signals.post_syncdb.connect(create_default_users,
    sender=auth_app, dispatch_uid="rah.management.create_default_users")