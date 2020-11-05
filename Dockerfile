FROM python:3.7-alpine
MAINTAINER Camilo Romero

# print output without buffering
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# create user for running app (avoid using root for security)
RUN adduser -D runUser
USER runUser