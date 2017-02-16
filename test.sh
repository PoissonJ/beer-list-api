#!/bin/bash

docker-compose -f docker-compose.test.yml build
docker-compose -f docker-compose.test.yml up -d
docker logs -f beerlistapi_web_1
EXIT_CODE="$(docker wait beerlistapi_web_1)"
if [ "${EXIT_CODE}" = "0" ]; then
    exit 0
else
    exit 1
fi