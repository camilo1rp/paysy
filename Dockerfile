FROM python:3.7-alpine as build
MAINTAINER Camilo Romero

# print output without buffering
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

RUN apt-get update && apt-get install -qy \
build-essential \
libssl-dev \
libffi-dev \
python-dev \
# clean up apt cache to keep image size smaller
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

FROM build as projectClone
RUN mkdir /app
WORKDIR /app
COPY ./app /app

FROM projectClone as entrypoint
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod ug+x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
VOLUME ["/etc/paysy-nginx/"]
# create user for running app (avoid using root for security)
#RUN adduser -D user
#USER user