#!/bin/bash

for file in `git diff --cached --name-only | grep .py$`
do
    if ! pylint -E --generated-members=objects,DoesNotExist "$file"
    then
        echo "$file did not pass the pylint tests"
        exit 1
    fi
done