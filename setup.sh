#!/bin/sh
# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
# Initialize database
cd bidwire
alembic upgrade head
