from celery import Celery, shared_task
from time import sleep
from app.config import SettingsFactory

config = SettingsFactory().get_settings('celery')

celery = Celery(__name__, broker=config.celery_broker)


@celery.task
def wait():
    sleep(10)
    print('task done!')
    return 1
