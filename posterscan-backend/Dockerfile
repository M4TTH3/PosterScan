FROM python:3.10-slim

WORKDIR /pyapp

COPY . .

RUN apt-get update
RUN apt-get upgrade
RUN apt-get install libzbar0

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD gunicorn --bind 0.0.0.0:5000 wsgi:app
