#!/usr/bin/env python
from datetime import datetime
from optparse import OptionParser
import shlex
import subprocess
import sys

class ServerAlias(object):
    def __init__(self, name, server=None, database=None, user=None, password=None, can_replace=False):
        self.name = name
        self.server = server
        self.database = database
        self.user = user
        self.password = password
        self.can_replace = can_replace
        
    def _connect_to_server(self, command=""):
        if self.server:
            command += "ssh -C %s " % self.server
        return command
        
    def dump_command(self, exclude=None):
        command = self._connect_to_server()
        command += "mysqldump -u %s -p%s %s " % (self.user, self.password, self.database)
        if exclude:
            command += " ".join(get_tables(self, exclude))
        return command
        
    def connect_command(self):
        command = self._connect_to_server()
        command += "mysql -u %s -p%s %s" % (self.user, self.password, self.database)
        return command
        
def backup_data(server_alias):
    now = datetime.today()
    backup_file = open("%s_%i%.2i%.2i_%.2i%.2i.sql" % (server_alias.name,
        now.year, now.month, now.day, now.hour, now.minute), "w")
    output = subprocess.Popen(shlex.split(server_alias.dump_command()),
        stdout=subprocess.PIPE).communicate()[0]
    backup_file.write(output)
    backup_file.close()
        
def get_tables(server_alias, exclude=None):
    if not exclude:
        exclude = []
    output = subprocess.Popen(shlex.split(server_alias.connect_command()),
        stdin=subprocess.PIPE, stdout=subprocess.PIPE).communicate("SHOW tables;")[0]
    return [t for t in output.split() if t not in exclude][1:]
        
def drop_tables(server_alias, exclude=None):
    tables = get_tables(server_alias, exclude)
    drop_statement = "SET FOREIGN_KEY_CHECKS=0;"
    drop_statement += "DROP TABLE " + ", ".join(tables) + ";"
    drop_statement += "SET FOREIGN_KEY_CHECKS=1;"
    subprocess.Popen(shlex.split(server_alias.connect_command()),
        stdin=subprocess.PIPE, stdout=subprocess.PIPE).communicate(drop_statement)[0]
        
def duplicate_data(duplicate_alias, replace_alias, exclude=None):
    dc = subprocess.Popen(shlex.split(duplicate_alias.dump_command(exclude)),
        stdout=subprocess.PIPE)
    rc = subprocess.Popen(shlex.split(replace_alias.connect_command()),
        stdin=dc.stdout, stdout=subprocess.PIPE)
    return rc.communicate()[0]
    
def parse_args(args):
    if len(args) != 4:
        print "You must specify a database to duplicate and a database to replace."
        print "Usage: %s <SETTINGS_FILE> <DUPLICATE_ALIAS> <REPLACE_ALIAS>" % args[0]
        sys.exit(2)
    
    settings = __import__(args[1])
    
    server_aliases = []
    for alias in (args[2], args[3]):
        server_alias = settings.MYSQLDUPLICATE_ALIASES.get(alias, None)
        if not server_alias:
            print "Alias %s has not been defined" % alias
            sys.exit(2)
        lowercase_dict = dict([(k.lower(), v) for k,v in server_alias.items()])
        server_aliases.append(ServerAlias(alias, **lowercase_dict))
    duplicate, replace = server_aliases
    
    if not replace.can_replace:
        print "Sorry, but %s can not be replaced" % args[3]
        sys.exit(2)
        
    return settings, duplicate, replace

def main():
    settings, duplicate, replace = parse_args(sys.argv)

    backup_data(replace)
    exclude = settings.MYSQLDUPLICATE_EXCLUDE if hasattr(settings, "MYSQLDUPLICATE_EXCLUDE") else None
    drop_tables(replace, exclude)
    print "Duplicating database..."
    duplicate_data(duplicate, replace, exclude)

if __name__ == "__main__":
    main()