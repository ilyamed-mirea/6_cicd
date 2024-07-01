#!/bin/sh

gunicorn --workers=1 -b=0.0.0.0:8080 help_students.wsgi:application