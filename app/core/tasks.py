from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.core.management import call_command
from paysy.celery import app


@shared_task
def add(x, y):
    return x + y


@shared_task
def check():
    print("updating transactions")
    call_command("sonda_transactions", )


app.conf.beat_schedule = {
    "run-this-every-five-minutes": {
        "task": "core.tasks.check",
        "schedule": 60.0
    }
}
