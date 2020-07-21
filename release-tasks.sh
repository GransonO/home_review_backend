#!/usr/bin/env bash
python -m spacy download en
python manage.py makemigrations
python manage.py migrate