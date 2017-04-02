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

To run the scraping process:
```
python main.py
```

# Code conventions

This codebase assumes Python 3, and the dockerized environment uses Python 3.6.
Code should be formatted in accordance with PEP8 (you can use
[autopep8](https://pypi.python.org/pypi/autopep8) to help with this).

# Future work

See our public Pivotal Tracker project for planned work: https://www.pivotaltracker.com/n/projects/1996883
