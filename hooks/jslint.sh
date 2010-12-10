#!/bin/bash

LINK=`readlink $0`
if [ -z $LINK ]
then
    THIS_DIR=`cd $(dirname $0) && pwd -P`
else
    THIS_DIR=`cd $(dirname $0)/$(dirname $LINK) && pwd -P`
fi
for file in `git diff --cached --name-only | grep .js$`
do
    if ! java -jar "$THIS_DIR/../tools/js.jar" "$THIS_DIR/../tools/jslint.js" "$THIS_DIR/../$file"
    then
        echo "$file did not pass the jslint tests"
        exit 1
    fi
done
