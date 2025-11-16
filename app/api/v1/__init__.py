from .chat import router as chat_router
from .embed import router as embed_router
from .model import router as models_router
from fastapi import (
    APIRouter
)
router_v1 = APIRouter(prefix="/v1")
router_v1.include_router(chat_router)
router_v1.include_router(embed_router)
router_v1.include_router(models_router)