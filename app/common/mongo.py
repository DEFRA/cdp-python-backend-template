from typing import Optional

from fastapi import Depends
from pymongo import AsyncMongoClient

from app.common.tls import cacerts
from app.config import config

client: Optional[AsyncMongoClient] = None
db = None


async def get_mongo_client() -> AsyncMongoClient:
    global client
    if not client:
        # Use the custom CA Certs from env vars if set.
        # We can remove this once we migrate to mongo Atlas.
        cert = cacerts.get("TRUSTSTORE_CDP")
        if cert:
            client = AsyncMongoClient(config.mongo_uri, tlsCAFile=cert)
        else:
            client = AsyncMongoClient(config.mongo_uri)
    return client


async def ensure_indexes(db):
    # Add indexes as needed
    pass


async def get_db(client: AsyncMongoClient = Depends(get_mongo_client)):
    global db
    if not db:
        db = client.get_database(config.mongo_database)
    return db
