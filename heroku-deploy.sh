#!/bin/bash -e

# Script to sync to master branch and push results to Heroku
# Then run setup.sh script to make sure all migrations are applied.
#
# Assumes that a Heroku remote is configured, and Heroku CLI is installed. See
# https://devcenter.heroku.com/articles/git for details.

git checkout master
git pull origin
git push heroku master
heroku run ./setup.sh
