from logging import getLogger
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends
from fastapi.middleware import Middleware
from asgi_logger import AccessLoggerMiddleware

from aws_embedded_metrics.config import get_config
from app.health.router import router as health_router
from app.example.router import router as example_router

from app.config import config
from app.common.mongo import get_mongo_client, get_db
from app.common.tracing import TraceIdMiddleware

logger = getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI ):
    # Startup
    client = await get_mongo_client()
    logger.info("mongo connected")
    yield
    # Shutdown
    if client:
        logger.info("mongo disconnected")
        await client.close()

app = FastAPI(lifespan=lifespan)

app.add_middleware(TraceIdMiddleware)

app.include_router(health_router)
app.include_router(example_router)

