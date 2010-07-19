from django.db.models import get_models, signals
from events import models as events_app

def create_default_events(app, created_models, verbosity, **kwargs):
    from events.models import EventType, Survey
    from django.core.management import call_command
    if EventType in created_models and kwargs.get('interactive', True):
        msg = "\nYou just installed the event_types table, would you like to install the " \
                "default set of event_types? (yes/no): "
        confirm = raw_input(msg)
        while 1:
            if confirm not in ('yes', 'no'):
                confirm = raw_input('Please enter either "yes" or "no": ')
                continue
            if confirm == 'yes':
                call_command("loaddata", "events/fixtures/event_types.json", verbosity=0, interactive=True)
            break
    if Survey in created_models and kwargs.get('interactive', True):
        msg = "\nYou just installed the survey table, would you like to install the " \
                "default set of surveys? (yes/no): "
        confirm = raw_input(msg)
        while 1:
            if confirm not in ('yes', 'no'):
                confirm = raw_input('Please enter either "yes" or "no": ')
                continue
            if confirm == 'yes':
                call_command("loaddata", "events/fixtures/surveys.json", verbosity=0, interactive=True)
            break
        
signals.post_syncdb.connect(create_default_events, sender=events_app, 
    dispatch_uid="rah.management.create_default_events")