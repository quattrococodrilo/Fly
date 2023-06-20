#!/usr/bin/env bash

/wait-for-it.sh -t 0 $DB_HOST:$DB_PORT --strict -- python manage.py runserver 0.0.0.0:8000
