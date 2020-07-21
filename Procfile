release: bash ./release-tasks.sh
web: gunicorn fluid.wsgi —-log-file -
worker: python3 manage.py qcluster