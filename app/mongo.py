from pymongo import MongoClient
from app.config import SettingsFactory
from app.models import Block, BlockChain
settings = SettingsFactory().get_settings('mongo')

client = MongoClient(settings.mongo_url, settings.mongo_port,
                     username=settings.mongo_login,
                     password=settings.mongo_password)

db = client.blockchain
collection = db.blocks

'''Some blockchain mongo funcs'''


def add_block(block):
    collection.insert_one(dict(block))


def get_last_block():
    block = collection.find_one(sort=[("id", -1)])
    if block:
        block = Block(**block)
    return block


def get_last_blocks(num):
    blocks = collection.find().sort('id', -1).limit(num)
    blockchain = []
    for block in blocks:
        blockchain.append(Block(**block))
    return BlockChain(blocks=blockchain)


def get_all_blocks():
    blocks = collection.find()
    blockchain = []
    for block in blocks:
        blockchain.append(block)
    return BlockChain(blocks=blockchain)


def get_relative_blocks(username):
    blocks = collection.find({"$or": [{"transaction.creditor": username},
                                      {"transaction.debtor": username}]})
    blockchain = []
    for block in blocks:
        blockchain.append(Block(**block))
    return blockchain
