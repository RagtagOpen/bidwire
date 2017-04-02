# BidWire

BidWire monitors [Commbuys](https://www.commbuys.com), the procurement
record system of the Commonwealth of Massachussets, and sends out notifications
when new bids are found.

# Developer setup

We provide a Docker-based environment for developing and testing BidWire.

Once you have installed [Docker](https://www.docker.com/get-docker), you can
start a new container to develop in with:

```
# run from the root of this repo
docker-compose run bidwire /bin/bash
```

This will start the Docker container and give you a shell prompt in it. It will
mount the source code inside the container at `/bidwire`, so you can edit code
outside of the container and see the changes inside it.

Once inside the container, install all dependencies with:
```
cd /bidwire
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

Bidwire depends on a Postgres database, and one is provided as part of the
docker-compose configuration. When you create the container, you will need to
initialize the database by running all migrations:

```
alembic upgrade head
```

Once your database is set up, you should be able to run the scraping process:
```
python main.py
```

# Code conventions

This codebase assumes Python 3, and the dockerized environment uses Python 3.6.
Code should be formatted in accordance with PEP8 (you can use
[autopep8](https://pypi.python.org/pypi/autopep8) to help with this).

# Database setup

BidWire depends on a Postgres database. This is provided for development as part
of the `docker-compose` setup -- a Postgres instance is available from the
container, at the host `database`.

In other environments, the env variable POSTGRES_ENDPOINT must be provided,
containing a complete Postgres connection string (e.g.
`postgres://username@hostname/database`).

## Migrations

We use [Alembic](http://alembic.zzzcomputing.com/) to manage database versioning
and migrations. To create a new database revision:
```
alembic revision -m "<revision name>"
```
Add your desired migration code to the newly generated file.

To run all migrations:
```
alembic upgrade head
```

# Future work

See our public Pivotal Tracker project for planned work: https://www.pivotaltracker.com/n/projects/1996883
