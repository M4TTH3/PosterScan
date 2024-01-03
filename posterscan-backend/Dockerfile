FROM python:3.10-slim

WORKDIR /pyapp

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD gunicorn --bind 0.0.0.0:5000 wsgi:app
