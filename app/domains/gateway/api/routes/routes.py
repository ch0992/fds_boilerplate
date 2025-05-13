"""
게이트웨이 서비스 API 라우터
"""
from fastapi import APIRouter

from app.domains.gateway.api.routes.file import router as file_router
from app.domains.gateway.api.routes.data import router as data_router
from app.domains.gateway.api.routes.log import router as log_router
from app.domains.gateway.api.routes.auth.auths import router as auth_router
from app.domains.gateway.api.routes.data import curs
from app.domains.gateway.clients.base_service_client import BaseServiceClient
from app.domains.gateway.clients.data_service_client import DataServiceClient
from app.domains.gateway.clients.log_service_client import LogServiceClient
from app.domains.gateway.clients.file_service_client import FileServiceClient
from app.common.config import settings
from app.domains.log.services.common.tracing import get_tracer

router = APIRouter()
router.include_router(auth_router)
router.include_router(file_router)
router.include_router(data_router)
router.include_router(log_router)
router.include_router(curs.router)

file_client = FileServiceClient(settings.FILE_SERVICE_URL)
data_client = DataServiceClient(settings.DATA_SERVICE_URL)
log_client = LogServiceClient(settings.LOG_SERVICE_URL)
tracer = get_tracer("gateway")

@router.get("/ping", summary="Health check", tags=["Health"])
async def ping():
    return {"message": "pong"}

@router.get("/file/ping", summary="File service health check", tags=["Health"])
async def file_ping():
    return {"message": "pong"}

@router.get("/data/ping", summary="Data service health check", tags=["Health"])
async def data_ping():
    return {"message": "pong"}

@router.get("/log/ping", summary="Log service health check", tags=["Health"])
async def log_ping():
    return {"message": "pong"}

