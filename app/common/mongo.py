from typing import Optional

from fastapi import Depends
from pymongo import AsyncMongoClient

from app.config import config

client: Optional[AsyncMongoClient] = None
db = None


async def get_mongo_client() -> AsyncMongoClient:
    global client
    if not client:
        # TODO: load tls certs
        client = AsyncMongoClient(config.mongo_uri)
    return client


async def ensure_indexes(db):
    # Add indexes as needed
    pass


async def get_db(client: AsyncMongoClient = Depends(get_mongo_client)):
    global db
    db = client.get_database(config.mongo_database)
    await ensure_indexes(db)
    return db
