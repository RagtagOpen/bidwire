#!/bin/bash -e

# Script to sync to master branch and push results to Heroku
# Assumes that a Heroku remote is configured. See
# https://devcenter.heroku.com/articles/git for details.

git checkout master
git pull origin
git push heroku master
