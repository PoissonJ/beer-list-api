#!/bin/bash

# print outputs and exit on first failure
set -xe

if [ $TRAVIS_BRANCH == "master" ] ; then

    # setup ssh agent, git config and remote
    eval "$(ssh-agent -s)"
    rm -rf .git
    git init
    # ssh-add ~/.ssh/travis_rsa
    git remote add deploy "travis@45.55.181.86:/opt/beer-list-api"
    git config user.name "Travis CI"
    git config user.email "jonathan.poisson777+travis@gmail.com"

    # commit compressed files and push it to remote
    # rm -f .gitignore
    # cp .travis/deployignore .gitignore
    git add .
    git status # debug
    git commit -m "Deploy"
    git push -f deploy HEAD:master
else
    echo "No deploy script for branch '$TRAVIS_BRANCH'"
fi
