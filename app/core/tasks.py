from __future__ import absolute_import, unicode_literals

from celery import shared_task

from paysy.celery import app


@shared_task
def add(x, y):
    return x + y


@app.task
def check():
    print("I am checking your stuff")


app.conf.beat_schedule = {
    "run-me-every-ten-seconds": {
        "task": "core.tasks.check",
        "schedule": 10.0
    }
}
