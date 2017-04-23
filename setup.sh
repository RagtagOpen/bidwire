#!/bin/sh
# Install dependencies
pip3 install -r requirements.txt
pip3 install -r requirements-dev.txt
# Initialize database
cd bidwire
alembic upgrade head
