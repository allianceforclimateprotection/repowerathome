import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'www.settings'
sys.path.append('/scripts')
sys.path.append('/scripts/www')

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()