import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
sys.path.append(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()