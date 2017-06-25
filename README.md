# BidWire

[![Build
Status](https://travis-ci.org/RagtagOpen/bidwire.svg?branch=master)](https://travis-ci.org/RagtagOpen/bidwire)

BidWire monitors government websites and sends out notifications to interested
parties when new content is found. We add new scrapers and notifiers as we get
requests for them.

For examples of the notifications sent by BidWire, see:
https://groups.google.com/forum/#!forum/bidwire-logs

# Contributing

If you'd like to get involved, see our [Contributor's
Guide](https://github.com/RagtagOpen/bidwire/blob/master/CONTRIBUTING.md).

For a concise example of how to add a new scraper + notifier pair, see: https://github.com/RagtagOpen/bidwire/pull/50

# Future work

See our public Pivotal Tracker project for planned work: https://www.pivotaltracker.com/n/projects/1996883


# Developer setup

This codebase assumes Python 3, with
[PEP8](https://www.python.org/dev/peps/pep-0008) coding style and
[Pytest](https://docs.pytest.org/en/latest/) for testing.

BidWire depends on a Postgres database being present. We provide a Docker-based
environment for developing and testing BidWire.

Once you have installed [Docker](https://www.docker.com/get-docker), you can
start a new container to develop in with:

```
# run from the root of this repo
docker-compose run bidwire /bin/bash
```

This will start the Docker container and give you a shell prompt in it. It will
mount the source code inside the container at `/bidwire`, so you can edit code
outside of the container and see the changes inside it.

Once inside the container, you can install all dependencies and initialize the database with:
```
cd bidwire
./setup.sh
```

After this, you should be able to run the scraping process:
```
python bidwire/main.py
```

To run tests:
```
pytest
```

To test specific functionality for a scraper/notifier for a site, there is a `manage.py` script available:
```
# Dry-run of City of Boston site - both scraping and notifying - sending email notification to me@gmail.com
python bidwire/manage.py dryrun --site CITYOFBOSTON --recipients me@gmail.com
```

```
# Only run notifier for City of Boston site, sending email notification to me@gmail.com
python bidwire/manage.py notify --site CITYOFBOSTON --recipients me@gmail.com
```

```
# Only run scraper for City of Boston site
python bidwire/manage.py scrape --site CITYOFBOSTON
```


# Database setup

BidWire depends on a Postgres database. This is provided for development as part
of the `docker-compose` setup -- a Postgres instance is available from the
container, at the host `database`.

In other environments, the env variable POSTGRES_ENDPOINT must be provided,
containing a complete Postgres connection string (e.g.
`postgres://username@hostname/database`).

## Schema migrations

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

# Acknowledgements

This project was born under the umbrella of [Ragtag](https://ragtag.org), a
volunteer team of technologists working for progressive change. Consider
[joining Ragtag](https://ragtag.org/join/) or
[donating](https://opencollective.com/ragtag) to help defray our operating
costs.

This project was instigated by [@jdegrazia](https://github.com/jdegrazia), who
continues to shepherd it with encouragement from
[@jillh510](https://github.com/jillh510) and coding from
[@anaulin](https://github.com/anaulin) and
[@klertmen](https://github.com/klertmen).
