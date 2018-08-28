from pymongo import MongoClient
import config.config as config


def init_db(db):
    client = MongoClient(config.host, config.port)
    return client[db]


def insert_row(collection, row, unique_key):
    key = {unique_key:row[unique_key]}
    collection.update(key,row,upsert=True)