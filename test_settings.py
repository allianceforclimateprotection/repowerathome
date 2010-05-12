try:
    from settings import *
except ImportError:
    print 'settings could not be imported'
    
DATABASE_ENGINE   = 'sqlite3'  # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.comments',
    'django.contrib.sites',
    'django.contrib.messages',
    'rah',
    'rateable',
    'rateable.tests',
    'records',
    'geo',
    'invite',
    'invite.tests',
    'basic.blog',
    'basic.inlines',
    'tagging',
    'twitter_app',
    'search_widget',
    'search_widget.tests',
    'groups',
    'sorl.thumbnail',
    'flagged',
    'flagged.tests',
    'django_extensions',
    'debug_toolbar',
    'dated_static',
    'notification',
    'actions',
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'HIDE_DJANGO_SQL': True,
    'SHOW_TOOLBAR_CALLBACK': lambda x: False,
}