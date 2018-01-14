# BidWire

[![Build
Status](https://travis-ci.org/RagtagOpen/bidwire.svg?branch=master)](https://travis-ci.org/RagtagOpen/bidwire)

BidWire monitors government websites and sends out notifications to interested
parties when new content is found. We add new scrapers and notifiers as we get
requests for them.

For examples of the notifications sent by BidWire, see:
https://groups.google.com/forum/#!forum/bidwire-logs

# Table of Contents

* [Overview](#overview)
* [Contributing](#contributing)
* [Future work](#future-work)
* [Developer setup](#developer-setup)
* [Database setup](#database-setup)
  * [Schema migrations](#schema-migrations)
* [Acknowledgements](#acknowledgements)

# Overview

BidWire runs as a daily batch job that performs the following steps:

* scrape the site and turn any new relevant content into structured data
* if new structured data is found, send an email notification with links to this new content

The list of notification recipients can be configured separately for each site
we monitor. For a list of the sites we monitor and the scrapers and notifiers for each, see
[SITE_CONFIG](https://github.com/RagtagOpen/bidwire/blob/master/bidwire/bidwire_settings.py#L52-L82). The entrypoint to the job is
[main.py](https://github.com/RagtagOpen/bidwire/blob/master/bidwire/main.py).

The daily BidWire job runs on a free Heroku instance, using the Heroku
Scheduler. We also use a free SendGrid account to send out the notification
emails.

For development purposes, we have a Docker setup; it exists only to make
your development environment for BidWire hermetic, and to make it easy to bring
up a Postgres instance locally. You can also do development on BidWire using a
virtual Python env, or whatever is most comfortable for you. BidWire does not
use Docker in production.

All configuration for BidWire happens via environment variables, which are read in the
[bidwire_settings.py](https://github.com/RagtagOpen/bidwire/blob/master/bidwire/bidwire_settings.py)
file. The configuration that tells BidWire which scraper, notifier and recipient
email addresses to use for each site is in the
[SITE_CONFIG](https://github.com/RagtagOpen/bidwire/blob/master/bidwire/bidwire_settings.py#L52-L82).

BidWire is backed by a Postgres database. The database is used as a way of
storing data we've seen before, so that we can tell what content is new and
therefore needs a notification. We don't use any fancy Postgres-specific stuff;
we could have as easily used plain text files or MySQL or some other simple way
to record and read back which items we've seen. You can get an idea of the data
model by looking at these Heroku Data Clips that query the production database:

* Bids: https://dataclips.heroku.com/coeeymksxotzrbuztwptowdeqqyy-All-bids-in-BidWire-database
* Documents: https://dataclips.heroku.com/psfoyasgswnykhgeiydvfhglkppr-All-Documents

We have two different models, `Bids` and `Documents` for historical reasons: we
originally thought that BidWire would monitor purchasing websites ("requests for
bids"), but ended up expanding it to monitor other kinds of sites, which led to
the more general Document model. BidWire uses [SQL
Alchemy](https://www.sqlalchemy.org/) to interact with the database from Python,
through the
[Bid](https://github.com/RagtagOpen/bidwire/blob/master/bidwire/bid.py) and
[Document](https://github.com/RagtagOpen/bidwire/blob/master/bidwire/document.py)
classes. We also use [Alembic](http://alembic.zzzcomputing.com/en/latest/) for
the (very occasional) database schema migration.

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
