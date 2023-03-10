#!/bin/bash

set -e

###############################
echo PACKAGE
cd djangorest
currentDate=$(date "+%d-%m-%Y")
docker build -t currency-conversion-api-djangorest .
docker image tag currency-conversion-api-djangorest fabbo/currency-conversion-api-djangorest:${currentDate}
docker image tag currency-conversion-api-djangorest fabbo/currency-conversion-api-djangorest:latest
docker image push fabbo/currency-conversion-api-djangorest:${currentDate}
docker image push fabbo/currency-conversion-api-djangorest:latest