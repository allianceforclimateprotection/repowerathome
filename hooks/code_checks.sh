#!/bin/bash

LINK=`readlink $0`
if [ -z $LINK ]
then
    THIS_DIR=`cd $(dirname $0) && pwd -P`
else
    THIS_DIR=`cd $(dirname $0)/$(dirname $LINK) && pwd -P`
fi
bash "$THIS_DIR/pylint.sh" && "$THIS_DIR/jslint.sh" && bash "$THIS_DIR/test.sh"
