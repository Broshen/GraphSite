web: gunicorn GraphSite.wsgi --log-file -
worker: celery worker --app=tasks.app