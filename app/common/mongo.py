from app.config import config
from fastapi import FastAPI, Depends
from pymongo import AsyncMongoClient, ASCENDING

client: AsyncMongoClient = None
db = None

async def get_mongo_client() -> AsyncMongoClient:
    global client
    if not client:
        # TODO: load tls certs
        client = AsyncMongoClient(config.mongo_uri)
    return client

async def get_db(client: AsyncMongoClient = Depends(get_mongo_client)):
    if not db:
        db = client.get_database(config.mongo_database)
        ensure_indexes(db)
    return db
