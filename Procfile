release: bash ./release-tasks.sh
web: gunicorn home_review.wsgi —-log-file -
worker: python manage.py qcluster