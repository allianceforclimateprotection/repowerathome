import gzip
import os

from django.core.management.color import color_style
from django.core.management.sql import custom_sql_for_model
from django.db import connections, transaction, DEFAULT_DB_ALIAS
from django.db.models import get_models, signals
from geo import models as geo_app

def create_default_locations(app, created_models, verbosity, **kwargs):
    from geo.models import Location
    from django.core.management import call_command
    if Location in created_models and kwargs.get('interactive', True):
        msg = "\nYou just installed the geo app, would you like to install the " \
                "standard set of Locations? (yes/no): "
        confirm = raw_input(msg)
        while 1:
            if confirm not in ('yes', 'no'):
                confirm = raw_input('Please enter either "yes" or "no": ')
                continue
            if confirm == 'yes':
                gunzip_location()
                
                connection = connections[DEFAULT_DB_ALIAS]
                cursor = connection.cursor()

                custom_sql = custom_sql_for_model(Location, color_style(), connection)
                if custom_sql:
                    if verbosity >= 1:
                        print "Installing custom SQL for geo.Location model"
                    try:
                        for sql in custom_sql:
                            cursor.execute(sql)
                    except Exception, e:
                        sys.stderr.write("Failed to install custom SQL for geo.Location model: %s\n" % e)
                        if show_traceback:
                            import traceback
                            traceback.print_exc()
                        transaction.rollback_unless_managed(using=DEFAULT_DB_ALIAS)
                    else:
                        transaction.commit_unless_managed(using=DEFAULT_DB_ALIAS)
                else:
                    if verbosity >= 2:
                        print "No custom SQL for geo.Location model"
                
                gzip_location()
            break
            
def gzip_location():
    path = os.path.join(os.path.dirname(__file__), "../sql/location.sql")
    os.system("gzip %s" % path)
    
def gunzip_location():
    path = os.path.join(os.path.dirname(__file__), "../sql/location.sql.gz")
    os.system("gunzip %s" % path)

signals.post_syncdb.connect(create_default_locations, sender=geo_app,
    dispatch_uid="rah.management.create_default_locations")