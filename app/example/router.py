from logging import getLogger

from fastapi import APIRouter, Depends

from app.common.mongo import get_db

router = APIRouter(prefix="/example")

logger = getLogger(__name__)


# remove this example route
@router.get("/")
async def root():
    logger.info("TEST ENDPOINT")
    return {"ok": True}


@router.get("/db")
async def db_query(db=Depends(get_db)):
    await db.foo.insert_one({"foo": "bar"})
    data = await db.foo.find_one({}, {"_id": 0})
    return {"ok": data}
