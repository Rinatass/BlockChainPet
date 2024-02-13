from pymongo import MongoClient
from app.config import SettingsFactory
from app.models import Block, BlockChain
settings = SettingsFactory().get_settings('mongo')

client = MongoClient(settings.mongo_url, settings.mongo_port,
                     username=settings.mongo_login,
                     password=settings.mongo_password)

db = client.blockchain
collection = db.blocks


def add_block(block):
    res = collection.insert_one(dict(block))


def get_last_block():
    block = Block(**collection.find_one(sort=[("id", -1)]))
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
    return BlockChain(blockchain)


def get_relative_blocks(username):
    blocks = collection.find({"$or": [{"transaction.creditor": username},
                                      {"transaction.debtor": username}]})
    blockchain = []
    for block in blocks:
        blockchain.append(Block(**block))
    return blockchain



"""db = client.blockchain
collection = db.blocks"""

"""my_data = {
    'kek': 2,
    '2': 'string'
}
db = client.test
collection = db.test

res = collection.insert_one(my_data)
print(res)
res = collection.find().limit(20)
for line in res:
    print(type(line))"""