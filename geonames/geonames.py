"""
This script converts a data dump available from geonames.org into a series of insert statements
that can be used to populate a database table. 

Two files are required to run the script and should be in the same directory as this script:
US.txt          (http://download.geonames.org/export/dump/US.zip)
admin2Codes.txt (http://download.geonames.org/export/dump/admin2Codes.txt)
"""

# Set up file handles
fin = open("US.txt")
fout = open("geonames.sql", "w")
fcounties = open("admin2Codes.txt")

# Vars to hold counts. Should be about 40,000 zips found
zipsFound = 0
countyCount = 0
lineCount = 0

# A lookup to convert state abbreviations into full state names
states = {
	"AL":"Alabama",
	"AK":"Alaska",
	"AZ":"Arizona",
	"AR":"Arkansas",
	"AF":"Armed Forces Africa",
	"AA":"Armed Forces Americas (Except Canada)",
	"AC":"Armed Forces Canada",
	"AE":"Armed Forces Europe",
	"AM":"Armed Forces Middle East",
	"AP":"Armed Forces Pacific",
	"CA":"California",
	"CO":"Colorado",
	"CT":"Connecticut",
	"DE":"Delaware",
	"DC":"District Of Columbia",
	"FL":"Florida",
	"GA":"Georgia",
	"GU":"Guam",
	"HI":"Hawaii",
	"ID":"Idaho",
	"IL":"Illinois",
	"IN":"Indiana",
	"IA":"Iowa",
	"KY":"Kansas",
	"KS":"Kentucky",
	"LA":"Louisiana",
	"ME":"Maine",
	"MD":"Maryland",
	"MA":"Massachusetts",
	"MI":"Michigan",
	"MN":"Minnesota",
	"MS":"Mississippi",
	"MO":"Missouri",
	"MT":"Montana",
	"NE":"Nebraska",
	"NV":"Nevada",
	"NH":"New Hampshire",
	"NJ":"New Jersey",
	"NM":"New Mexico",
	"NY":"New York",
	"NC":"North Carolina",
	"ND":"North Dakota",
	"OH":"Ohio",
	"OK":"Oklahoma",
	"OR":"Oregon",
	"PA":"Pennsylvania",
	"PR":"Puerto Rico",
	"RI":"Rhode Island",
	"SC":"South Carolina",
	"SD":"South Dakota",
	"TN":"Tennessee",
	"TX":"Texas",
	"UT":"Utah",
	"VT":"Vermont",
	"VA":"Virginia",
	"VI":"Virgin Islands",
	"WA":"Washington",
	"WV":"West Virginia",
	"WI":"Wisconsin",
	"WY":"Wyoming"
}

# Load County names into memory
counties = {}
for line in fcounties:
    if not line.startswith("US"):
        continue
    else:
        parts = line.split("\t")
        code = parts[0]
        counties[code] = parts[1]
        countyCount += 1



# Work through the main file and generate SQL
for line in fin:
    lineCount += 1
    line = line.strip()
    line = str(line)
    parts = line.split("\t")

    # See if there is an alternate name
    if parts[3]:
        # If so, split on the comma and go through each split element.
        altparts = parts[3].split(",")
        for altpart in altparts:
            # If we have a number, it's a zipcode!
            if altpart.isdigit():
                name     = parts[1]
                zipcode  = altpart
                st       = parts[10]
                state    = states[parts[10]]
                lon      = parts[5]
                lat      = parts[4]
                pop      = parts[14]
                timezone = parts[17]

                # DC doesn't have an counties in admin2Codes.txt
                if st == "DC":
                    county = "District of Columbia"
                else:
                    county = counties["US." + st + "." + parts[11]]
                
                # Write a line of SQL
                fout.write("INSERT INTO `rah_geo` (`name`,`zipcode`,`county`,`st`,`state`,`lon`,`lat`,`pop`,`timezone`) ")
                fout.write('VALUES ("%s","%s","%s","%s","%s","%s","%s",%s,"%s");\n' % (name, zipcode, county, st, state, lon, lat, pop, timezone)) 
                zipsFound += 1
            else:
                continue

# Close file handles
fin.close()
fout.close()
fcounties.close()

# Print out some totals
print "Total Counties: " + str(countyCount)
print "Zips Found: "     + str(zipsFound)
print "Total Lines: "    + str(lineCount)
