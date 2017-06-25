FROM python:3.6
WORKDIR /bidwire
ADD requirements.txt .
ADD requirements-dev.txt .
RUN pip3 install -r requirements-dev.txt
ADD . .
