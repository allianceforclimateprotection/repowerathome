from optparse import make_option
import os
import re
import sys

from django.conf import settings
from django.core.management.base import NoArgsCommand
from django.core.management.color import no_style
from django.db import connections, models, transaction, DEFAULT_DB_ALIAS
from django.utils.importlib import import_module

from migrations.models import Migrate

def custom_migrate_sql(style, connection):
    opts = Migrate._meta
    app_dir = os.path.normpath(os.path.dirname(models.get_app(Migrate._meta.app_label).__file__))
    output = []

    # Some backends can't execute more than one SQL statement at a time,
    # so split into separate statements.
    statements = re.compile(r";[ \t]*$", re.M)

    # Find custom SQL, if it's available.
    backend_name = connection.settings_dict['ENGINE'].split('.')[-1]
    sql_files = [os.path.join(app_dir, "%s.%s.sql" % (opts.object_name.lower(), backend_name)),
                 os.path.join(app_dir, "%s.sql" % opts.object_name.lower())]
    for sql_file in sql_files:
        if os.path.exists(sql_file):
            fp = open(sql_file, 'U')
            for statement in statements.split(fp.read().decode(settings.FILE_CHARSET)):
                # Remove any comments from the file
                statement = re.sub(ur"--.*([\n\Z]|$)", "", statement)
                if statement.strip():
                    output.append(statement + u";")
            fp.close()

    return output

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('--database', action='store', dest='database',
            default=DEFAULT_DB_ALIAS, help='Nominates a database to synchronize. '
                'Defaults to the "default" database.'),
    )
    help = "Execute all of the SQL statments found in the migrations/sql/migrate.sql file."

    @transaction.commit_manually
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
        
        custom_sql = custom_migrate_sql(self.style, connection)
        if custom_sql:
            if verbosity >= 1:
                print "Running SQL migrations in migrations/sql/migrate.sql"
            try:
                for sql in custom_sql:
                    cursor.execute(sql.replace("%", "%%"))
            except Exception, e:
                sys.stderr.write("Failed to run custom SQL in migrations/sql/migrate.sql: %s" % e)
                if show_traceback:
                    import traceback
                    traceback.print_exc()
                transaction.rollback(using=db)
            else:
                transaction.commit(using=db)
        else:
            transaction.rollback(using=db)
            if verbosity >= 2:
                print "No SQL migrations to run"
