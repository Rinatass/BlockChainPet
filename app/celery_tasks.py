from celery import Celery
from app.config import SettingsFactory
from app.mongo import add_block
from app.blockchain import calculate_hash
from app.models import Block, Transaction
config = SettingsFactory().get_settings('celery')

celery = Celery(__name__, broker=config.celery_broker)


@celery.task
def process_block(transaction, previous_block):
    previous_block = Block(**previous_block)
    transaction = Transaction(**transaction)
    hashable = transaction.get_hashable() + previous_block.get_hashable()
    hash_, proof = calculate_hash(hashable, 15)

    block = Block(id=previous_block.id + 1,
                  transaction=dict(transaction),
                  previous_block_hash=previous_block.hash,
                  proof=proof,
                  hash=hash_)
    add_block(block)

