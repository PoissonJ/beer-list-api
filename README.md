[![Build Status](https://travis-ci.org/PoissonJ/beer-list-api.svg?branch=master)](https://travis-ci.org/PoissonJ/beer-list-api)

# Beer List Api

Api for the beer list IOS app - **ABANDONED**

Web service includes admin section for CRUD operations

## Running locally

- Install docker and docker-compose
- Run `sh build.sh` to build the docker images and have them run in the terminal
- Visit http://0.0.0.0:5000 to get to admin login screen
- Sample user is created with username `admin` and password `password`

Tests can be run with `sh test.sh`.

## Technology

- Flask
- MongoDB
- py.test

Deployment achieved with:

- TravisCI
- Digital Ocean

# TODO

- Add swagger API docs
