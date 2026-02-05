import os
from pymongo import MongoClient
from typing import Optional
from pymongo.collection import Collection

_client: Optional[MongoClient] = None


def _get_client() -> MongoClient:
    global _client

    if _client is not None:
        return _client

    mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    _client = MongoClient(mongo_url)
    return _client


def get_db_name() -> str:
    return os.getenv("MONGO_DB", "client_webservice")


def get_clients_collection() -> Collection:
    db_name = get_db_name()
    collection_name = os.getenv("MONGO_CLIENTS_COLLECTION", "clients")

    client = _get_client()
    db = client[db_name]
    return db[collection_name]
