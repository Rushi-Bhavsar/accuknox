#!/bin/bash

python manage.py migrate --no-input > /opt/git/python/migrate.out 2>&1
python manage.py collectstatic --no-input > /opt/git/python/collectstatic.out 2>&1
gunicorn accuknox.wsgi:application --capture-output --log-level critical --bind 0.0.0.0:8010 --access-logfile "/applog/guni_access_app_log.log" --error-logfile "/applog/guni_error_app_log.log"