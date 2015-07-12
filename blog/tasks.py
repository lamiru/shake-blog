from celery import shared_task
from time import sleep


@shared_task
def slow_sum(x, y):
    sleep(3)
    return x + y
