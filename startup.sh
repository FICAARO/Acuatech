#!/bin/bash
DIRECTORY="env"
if [ -d "$DIRECTORY" ]; then
  echo "$DIRECTORY does exist."
else
  python -m venv env
  source env/bin/activate
  pip install -r requieriments.txt

fi

python manage.py runserver