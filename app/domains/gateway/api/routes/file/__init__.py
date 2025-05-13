from fastapi import APIRouter
from fastapi import Header, HTTPException
from . import sqls, s3, zips, topics, aliases, upload

router = APIRouter(prefix="/file")
router.include_router(sqls.router)
router.include_router(s3.router)
router.include_router(zips.router)
router.include_router(topics.router)
router.include_router(aliases.router)
router.include_router(upload.router)

