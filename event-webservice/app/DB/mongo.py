from pymongo import MongoClient
from Core.config import settings

mongo_client = MongoClient(settings.mongo_uri)
mongo_db = mongo_client[settings.mongo_db_name]


def get_clients_collection():
    return mongo_db["clients"]
