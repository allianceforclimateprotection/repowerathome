#!/usr/bin/env python
"""
The intent of the mysqlduplicate.py module is to automate the procedure in which one database's
data is replaced by another's.  This module works on both databases that are housed locally and 
those that can be accessed via SSH.  Note that if you want to access a remote database, you must
have SSH keys already in place to connect to the remote server.  Also note that if would like to
connect to a server with a different username, use the "<username>@<servername>" syntax.

Requirements:
    You must provide a, or use the default, settings module to define at least 2 server aliases.
    The server aliases are used to describe what server you would like to duplicate and what
    server you would like to replace.  For example you could have the following in your
    settings.py file:
    
        MYSQLDUPLICATE_ALIASES = {
            "local": {
                "DATABASE": "test",
                "USER": "root",
                "PASSWORD": ";qewrgcas;lkdf"
                "CAN_REPLACE": True,
            },
            "production": {
                "server": "admin@server.com"
                "DATABASE": "production",
                "HOST": "mysqlserver@server.com",
                "USER": "root",
                "PASSWORD": ";qewrgcas;lkdf"
            }
        }
    
    Notice by default a database can not be replaced, if the database needs to be replaceable, 
    you must set the "CAN_REPLACE" property to True.  Also if a server name is not provided it 
    assumes that the databased is stored locally.
    
    Also the "HOST" property is optional in cases where the database is located on the server you
    are connecting to.  But if for instance you need to ssh into a server that is communicating 
    with a mysql database on another server, you will need to provide "HOST".
    
Usage:
    To execute the this module you can run something like the following:
        python mysqlduplicate.py --settings local_settings production local
            or
        python mysqlduplicate.py production local (in this example the default module 'settings' will be used)
"""
from datetime import datetime
from optparse import OptionParser
import shlex
import subprocess
import sys

class ServerAlias(object):
    """
    ServerAlias is a wrapper class for variables describing the location of a MYSQL database.
    It needs to know of a server, database name, database user and database password.  It makes
    the assumption that any server you need to connect to via SSH can be done so with your 
    existing SSH keys.
    """
    def __init__(self, name, server=None, database=None, user=None, password=None, 
        can_replace=False, host="127.0.0.1"):
        self.name = name
        self.server = server
        self.database = database
        self.host = host
        self.user = user
        self.password = password
        self.can_replace = can_replace
        
    def _connect_to_server(self, command=""):
        if self.server:
            command += "ssh -C %s " % self.server
        return command
        
    def dump_command(self, exclude=None):
        """
        Create a MYSQL command that can be used to dump the contents of this database.  Optionally
        include a list of tables to be excluded.
        """
        command = self._connect_to_server()
        command += "mysqldump -h %s -u %s -p'%s' %s " % (self.host, self.user, self.password, self.database)
        if exclude:
            command += " ".join(self.get_tables(exclude))
        return command
        
    def connect_command(self):
        """
        Create a MYSQL command that can be used to connect to the database, this is useful for
        createing connections and piping SQL statements into its STDIN stream.  Optionally include
        a list of tables to be excluded.
        """
        command = self._connect_to_server()
        command += "mysql -h %s -u %s -p'%s' %s" % (self.host, self.user, self.password, self.database)
        return command
        
    def backup_data(self):
        """
        Backup all of the data within this MYSQL database and export it to a named/timestamped
        file within the current working directory.
        """
        now = datetime.today()
        backup_file = open("%s_%i%.2i%.2i_%.2i%.2i.sql" % (self.name,
            now.year, now.month, now.day, now.hour, now.minute), "w")
        output = subprocess.Popen(shlex.split(self.dump_command()),
            stdout=subprocess.PIPE).communicate()[0]
        backup_file.write(output)
        backup_file.close()
        
    def get_tables(self, exclude=None):
        """
        Get a list of all the tables within this database.  Optionally provide a list of tables
        to be excluded in the return list.
        """
        if not exclude:
            exclude = []
        output = subprocess.Popen(shlex.split(self.connect_command()),
            stdin=subprocess.PIPE, stdout=subprocess.PIPE).communicate("SHOW tables;")[0]
        return [t for t in output.split() if t not in exclude][1:]
        
    def drop_tables(self, exclude=None):
        """
        Drop all of the tables within this database.  Optionally provide a list of tables
        that you would like to have preserved.
        """
        tables = self.get_tables(exclude)
        drop_statement = "SET FOREIGN_KEY_CHECKS=0;"
        drop_statement += "DROP TABLE " + ", ".join(tables) + ";"
        drop_statement += "SET FOREIGN_KEY_CHECKS=1;"
        subprocess.Popen(shlex.split(self.connect_command()),
            stdin=subprocess.PIPE, stdout=subprocess.PIPE).communicate(drop_statement)[0]
        
def duplicate_data(duplicate_alias, replace_alias, exclude=None):
    """
    Duplicate the data in the database and pipe this data into the replacememnt database. Optionally
    you can provide an exclude list of tables not to be replaced.
    """
    dc = subprocess.Popen(shlex.split(duplicate_alias.dump_command(exclude)),
        stdout=subprocess.PIPE)
    rc = subprocess.Popen(shlex.split(replace_alias.connect_command()),
        stdin=dc.stdout, stdout=subprocess.PIPE)
    return rc.communicate()[0]
    
def parse_args(args):
    usage = "usage: %prog [options] <DUPLICATE_ALIAS> <REPLACE_ALIAS>"
    parser = OptionParser(usage=usage)
    parser.add_option("-s", "--settings", dest="settings", default="settings",
        help="MODULE to load configurations from [settings]", metavar="MODULE")
    options, args = parser.parse_args()
    
    if len(args) != 2:
        parser.print_help()
        sys.exit(2)
    
    settings = __import__(options.settings)
    
    server_aliases = []
    for alias in (args[0], args[1]):
        server_alias = settings.MYSQLDUPLICATE_ALIASES.get(alias, None)
        if not server_alias:
            print "Alias %s has not been defined" % alias
            parser.print_help()
            sys.exit(2)
        lowercase_dict = dict([(k.lower(), v) for k,v in server_alias.items()])
        server_aliases.append(ServerAlias(alias, **lowercase_dict))
    duplicate, replace = server_aliases
    
    if not replace.can_replace:
        print "Sorry, but %s can not be replaced" % replace.name
        parser.print_help()
        sys.exit(2)
        
    return settings, duplicate, replace

def main():
    settings, duplicate, replace = parse_args(sys.argv)
    replace.backup_data()
    exclude = settings.MYSQLDUPLICATE_EXCLUDE if hasattr(settings, "MYSQLDUPLICATE_EXCLUDE") else None
    replace.drop_tables(exclude)
    print "Duplicating database..."
    duplicate_data(duplicate, replace, exclude)

if __name__ == "__main__":
    main()