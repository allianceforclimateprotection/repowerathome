#!/bin/sh

python manage.py loaddata fixtures/auth.json
python manage.py loaddata basic/blog/fixtures/post.json
python manage.py loaddata actions/fixtures/action.json