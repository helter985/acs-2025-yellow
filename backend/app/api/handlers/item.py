from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.item_schema import  ItemOut
from app.services.item_service import ItemService
from app.models.item_model import ItemModel
from pymongo import errors

item_router = APIRouter()


@item_router.get("/item/{id}", summary="Get item details", response_model=ItemOut)
async def get_item(id: str):
    item = await ItemService.get_item_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return item


@item_router.get("/", summary="Show all items", response_model=list[ItemOut])
async def get_items():
    try:
        return await ItemService.get_items()
    except errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No items found"
        )
        