#!/usr/bin/env python
"""
This script converts a data dump available from geonames.org into a series of insert statements
that can be used to populate theh location table. 

The data file needed for this script can be found at:
US.txt          (http://download.geonames.org/export/zip/US.zip)
"""
import sys
import csv

if len(sys.argv) != 2:
    print "Please provide the file you would like to parse"
    sys.exit()
postalcodes_file = sys.argv[1]

for row in csv.reader(open(postalcodes_file), delimiter="\t"):
    name = row[2]
    zipcode = row[1]
    county = row[5]
    st = row[4]
    state = row[3]
    lat = row[9]
    lon = row[10]
    print("INSERT INTO `geo_location` (`name`,`zipcode`,`county`,`st`,`state`,`lon`,`lat`,`recruit`) ")
    print('VALUES ("%s","%s","%s","%s","%s","%s","%s",0);\n' % (name, zipcode, county, st, state, lon, lat))