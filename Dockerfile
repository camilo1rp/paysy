FROM python:3.7-alpine as build
MAINTAINER Camilo Romero

# print output without buffering
ENV PYTHONUNBUFFERED 0

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev \
        libressl-dev musl-dev libffi-dev

RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

FROM build as projectClone
RUN mkdir /app
WORKDIR /app
COPY ./app /app

#FROM projectClone as entrypoint
#COPY docker-entrypoint.sh /docker-entrypoint.sh
#RUN chmod ug+x /docker-entrypoint.sh
#ENTRYPOINT ["/docker-entrypoint.sh"]
#VOLUME ["/etc/paysy-nginx/"]
# create user for running app (avoid using root for security)
#RUN adduser -D user
#USER user