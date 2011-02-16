#!/bin/bash

if ! ./manage.py test --settings=test_settings rah invite groups actions commitments events records rateable flagged source_tracking messaging search_widget tagging badges
then
    echo "-----"
    echo "Some of your tests failed, you must fix these first before you can commit."
    echo "Alternatively you can run 'git commit --no-verify' to force it in."
    exit 1
fi
