from fastapi import APIRouter
from app.api.handlers import item


router = APIRouter()


router.include_router(item.item_router, prefix="/item", tags=["item"])
