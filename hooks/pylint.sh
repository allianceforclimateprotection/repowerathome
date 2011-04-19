#!/bin/bash
LINK=`readlink $0`
if [ -z $LINK ]
then
    THIS_DIR=`cd $(dirname $0) && pwd -P`
else
    THIS_DIR=`cd $(dirname $0)/$(dirname $LINK) && pwd -P`
fi

for file in `git diff --cached --name-only | grep .py$`
do  
    if ! pylint -E --disable=E1102 --rcfile="$THIS_DIR/pylint.ini" "$file"
    then
        echo "$file did not pass the pylint tests"
        exit 1
    fi
done
