from django.db.models import get_models, signals
from messaging import models as messaging_app

def create_default_messages(app, created_models, verbosity, **kwargs):
    from messaging.models import Message, ABTest
    from django.core.management import call_command
    if Message in created_models and ABTest in created_models and kwargs.get('interactive', True):
        call_command("loaddata", "messaging/fixtures/initial_data.json", verbosity=0, interactive=True)
        msg = "\nYou just installed the message and ab_test tables, would you like to install the " \
                "default set of messages for commitment streams? (yes/no): "
        confirm = raw_input(msg)
        while 1:
            if confirm not in ('yes', 'no'):
                confirm = raw_input('Please enter either "yes" or "no": ')
                continue
            if confirm == 'yes':
                call_command("loaddata", "messaging/fixtures/commitment.json", verbosity=0, interactive=True)
            break
        
signals.post_syncdb.connect(create_default_messages, sender=messaging_app, 
    dispatch_uid="rah.management.create_default_messages")