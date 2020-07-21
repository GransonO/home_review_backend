release: bash ./release-tasks.sh
web: gunicorn fluid.wsgi —-log-file -
worker: python manage.py qcluster