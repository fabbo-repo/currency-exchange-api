#!/bin/bash

set -e

###############################
echo STATIC
cd backend-djangorest/djangorest/src
pip install -r requirements.txt
python manage.py makemigrations
cd -
