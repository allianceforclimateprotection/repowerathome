from optparse import make_option
import sys

from django.conf import settings
from django.core.management.base import NoArgsCommand
from django.core.management.color import no_style
from django.core.management.sql import custom_sql_for_model
from django.db import connections, transaction, DEFAULT_DB_ALIAS
from django.utils.importlib import import_module

from migrations.models import Migrate

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('--database', action='store', dest='database',
            default=DEFAULT_DB_ALIAS, help='Nominates a database to synchronize. '
                'Defaults to the "default" database.'),
    )
    help = "Execute all of the SQL statments found in the migrations/sql/migrate.sql file."

    def handle_noargs(self, **options):
        verbosity = int(options.get('verbosity', 1))
        interactive = options.get('interactive')
        show_traceback = options.get('traceback', False)

        self.style = no_style()

        # Import the 'management' module within each installed app, to register
        # dispatcher events.
        for app_name in settings.INSTALLED_APPS:
            try:
                import_module('.management', app_name)
            except ImportError, exc:
                # This is slightly hackish. We want to ignore ImportErrors
                # if the "management" module itself is missing -- but we don't
                # want to ignore the exception if the management module exists
                # but raises an ImportError for some reason. The only way we
                # can do this is to check the text of the exception. Note that
                # we're a bit broad in how we check the text, because different
                # Python implementations may not use the same text.
                # CPython uses the text "No module named management"
                # PyPy uses "No module named myproject.myapp.management"
                msg = exc.args[0]
                if not msg.startswith('No module named') or 'management' not in msg:
                    raise

        db = options.get('database', DEFAULT_DB_ALIAS)
        connection = connections[db]
        cursor = connection.cursor()

        transaction.commit_unless_managed(using=db)
        
        custom_sql = custom_sql_for_model(Migrate, self.style, connection)
        if custom_sql:
            if verbosity >= 1:
                print "Running SQL migrations in migrations/sql/migrate.sql"
            try:
                for sql in custom_sql:
                    cursor.execute(sql)
            except Exception, e:
                sys.stderr.write("Failed to run custom SQL in migrations/sql/migrate.sql: %s" % e)
                if show_traceback:
                    import traceback
                    traceback.print_exc()
                transaction.rollback_unless_managed(using=db)
            else:
                transaction.commit_unless_managed(using=db)
        else:
            if verbosity >= 2:
                print "No SQL migrations to run"
