#!/usr/bin/env bash

/wait-for-it.sh -t 0 db:3306 --strict -- python manage.py runserver 0.0.0.0:8000
