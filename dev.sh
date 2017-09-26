#!/bin/bash

python manage.py runserver &
./redis-server.exe &
wait

