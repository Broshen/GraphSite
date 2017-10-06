#!/bin/bash

./redis-server.exe & python manage.py runserver & wait

# run celery task seperately:
# celery -A GraphSite worker -l info