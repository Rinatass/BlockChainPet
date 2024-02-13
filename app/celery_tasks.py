from celery import Celery, shared_task
from time import sleep
from app.config import SettingsFactory
from app.mongo import add_block
config = SettingsFactory().get_settings('celery')

celery = Celery(__name__, broker=config.celery_broker)


@celery.task
def wait():
    sleep(10)
    print('task done!')
    return 1


@celery.task
def proceed_block(block):
    add_block(block)
    pass

# celery_tasks.wait.delay()
