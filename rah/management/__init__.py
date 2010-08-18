from django.db.models import get_models, signals
from django.contrib.auth import models as auth_app
from django.contrib.sites import models as sites_app
from django.core.management import call_command

def create_default_users(app, created_models, verbosity, **kwargs):
    from django.contrib.auth.models import User
    if User in created_models and kwargs.get('interactive', True):
        msg = "\nYou just installed Django's auth system, would you like to install the " \
                "standard set of RAH users? (yes/no): "
        confirm = raw_input(msg)
        while 1:
            if confirm not in ('yes', 'no'):
                confirm = raw_input('Please enter either "yes" or "no": ')
                continue
            if confirm == 'yes':
                call_command("loaddata", "fixtures/auth.json", verbosity=0, interactive=True)
            break
            
def set_django_site(app, created_models, verbosity, **kwargs):
    from django.contrib.sites.models import Site
    if Site in created_models and kwargs.get('interactive', True):
        msg = "\nYou just installed Django's sites system, would you like to set a default "\
                "domain? (yes/no): "
        confirm = raw_input(msg)
        while 1:
            if confirm not in ('yes', 'no'):
                confirm = raw_input('Please enter either "yes" or "no": ')
                continue
            if confirm == 'yes':
                domain = raw_input('What is the name of your domain? ')
                Site.objects.all().delete()
                Site.objects.create(id=1, domain=domain, name=domain)
            break
            
signals.post_syncdb.connect(create_default_users, sender=auth_app,
    dispatch_uid="rah.management.create_default_users")
signals.post_syncdb.connect(set_django_site, sender=sites_app,
    dispatch_uid="rah.management.set_django_site")