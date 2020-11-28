#!/bin/bash
set -e

# read docker secrets into env variables
export DJANGO_SUPERUSER_PASSWORD=passwordTest123
export DJANGO_SUPERUSER_MAIL=paysyadmin@paysy.com
export DB_PASSWORD=supersecretpassword
export SECRET_KEY=[6d\va#)hx+4NSB4

# run db migrations (retry on error)
while ! python3 /app/manage.py migrate 2>&1; do
  sleep 5
done

# Create Superuser if required
if [ "$DJANGO_SKIP_SUPERUSER" == "true" ]; then
  echo "↩️ Skip creating the superuser"
else
  if [ -z ${DJANGO_SUPERUSER_NAME+x} ]; then
    DJANGO_SUPERUSER_NAME='admin'
  fi
  if [ -z ${DJANGO_SUPERUSER_MAIL+x} ]; then
    DJANGO_SUPERUSER_MAIL='admin@example.com'
  fi
  if [ -z ${DJANGO_SUPERUSER_PASSWORD+x} ]; then
    if [ -f "/run/secrets/django_superuser_password" ]; then
      DJANGO_SUPERUSER_PASSWORD=$DJANGO_SUPERUSER_PASSWORD
    else
      DJANGO_SUPERUSER_PASSWORD='Paysyadmin20%'
    fi
  fi

python3 /app/manage.py shell << END
from django.contrib.auth.models import User
if not User.objects.filter(username='${DJANGO_SUPERUSER_NAME}'):
  u=User.objects.create_superuser('${DJANGO_SUPERUSER_NAME}', '${DJANGO_SUPERUSER_MAIL}', '${DJANGO_SUPERUSER_PASSWORD}')
END
  echo "Superuser Username: ${DJANGO_SUPERUSER_NAME}, E-mail: ${DJANGO_SUPERUSER_MAIL}"
fi

python3 /app/manage.py collectstatic --noinput

#move to app directory
cd /app/

daphne -b app -p 8080 paysy.asgi:application
