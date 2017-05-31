#!/bin/sh
# Install dependencies
pip3 install -r requirements.txt
pip3 install -r requirements-dev.txt
# Run all database migrations
cd bidwire
alembic upgrade head
