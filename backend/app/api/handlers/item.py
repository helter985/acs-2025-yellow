from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.item_schema import  ItemOut, ItemCreate
from app.services.item_service import ItemService
from app.models.item_model import ItemModel
from pymongo import errors

item_router = APIRouter(prefix="/items")


@item_router.get("/{id}", summary="Get item by id", response_model=ItemOut)
async def get_item(id: str):
    item = await ItemService.get_item_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return item


@item_router.get("/{barcode}", summary="Get item by barcode", response_model=ItemOut)
async def get_item_by_barcode(barcode: str):
    item = await ItemService.get_item_by_barcode(barcode)
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
        

@item_router.post("/create-item", summary="Create a new item", response_model=ItemOut)
async def item_candidate(data: ItemCreate):
    try:
        return await ItemService.create_item(data)
    except errors.DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Candidate already registered"
        )

