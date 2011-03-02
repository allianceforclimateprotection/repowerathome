try:
    from settings import *
except ImportError:
    print 'settings could not be imported'

DATABASE_ENGINE   = 'sqlite3'  # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.

CACHE_BACKEND = 'dummy://'

INSTALLED_APPS = list(INSTALLED_APPS) + [
    'rateable.tests',
    'invite.tests',
    'search_widget.tests',
    'flagged.tests',
    'messaging.tests',
]

LOGIN_URL = "/login/"

USE_TESTING_WIDGET = False

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'HIDE_DJANGO_SQL': True,
    'SHOW_TOOLBAR_CALLBACK': lambda x: False,
}
