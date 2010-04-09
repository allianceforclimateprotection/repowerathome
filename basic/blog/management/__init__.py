from django.db.models import get_models, signals
from django.contrib.auth import models as auth_app

def create_default_posts(app, created_models, verbosity, **kwargs):
    from basic.blog.models import Post
    from django.core.management import call_command
    if Post in created_models and kwargs.get('interactive', True):
        msg = "\nYou just installed the basic blog system, would you like to install the " \
                "default set of blog posts? (yes/no): "
        confirm = raw_input(msg)
        while 1:
            if confirm not in ('yes', 'no'):
                confirm = raw_input('Please enter either "yes" or "no": ')
                continue
            if confirm == 'yes':
                call_command("loaddata", "basic/blog/fixtures/post.json", verbosity=0, interactive=True)
            break

signals.post_syncdb.connect(create_default_posts,
    sender=auth_app, dispatch_uid="rah.management.create_default_posts")