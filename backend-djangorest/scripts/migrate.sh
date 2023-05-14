#!/bin/bash

set -e

###############################
docker-compose run --entrypoint "sh" api -c "python manage.py migrate"