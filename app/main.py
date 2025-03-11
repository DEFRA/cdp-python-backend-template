from contextlib import asynccontextmanager
from logging import getLogger

from fastapi import FastAPI

from app.common.mongo import get_mongo_client
from app.common.tracing import TraceIdMiddleware
from app.example.router import router as example_router
from app.health.router import router as health_router

logger = getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
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
