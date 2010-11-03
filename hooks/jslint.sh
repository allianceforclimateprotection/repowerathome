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
    if ! rhino "$THIS_DIR/../static/lint/jslint.js" "$file"
    then
        echo "$file did not pass the jslint tests"
        exit 1
    fi
done