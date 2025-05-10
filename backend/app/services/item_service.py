from app.schemas.item_schema import ItemOut, ItemCreate, ItemUpdate
from app.models.item_model import ItemModel
from fastapi import HTTPException, status
from typing import List
from bson import ObjectId


class ItemService:
    @staticmethod
    async def create_item(item_data: ItemCreate) -> ItemOut:
        try:
            item = ItemModel(
                name=item_data.name,
                price=item_data.price,
            )
            await item.save()
            return ItemOut(
                id=str(item.id),
                name=item.name,
                price=item.price,
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    @staticmethod
    async def get_item_by_id(id: str) -> ItemOut:
        item = await ItemModel.find_one(ItemModel.id == ObjectId(id))
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return ItemOut(
            id=str(item.id),
            name=item.name,
            price=item.price,
        )
    
    @staticmethod
    async def get_items() -> List[ItemOut]:
        items = await ItemModel.all().to_list()
        return [
            ItemOut(
                id=str(item.id),
                name=item.name,
                price=item.price,
            ) for item in items
        ]
    
    @staticmethod
    async def update_item(id: str, item_data: ItemUpdate) -> ItemOut:
        item = await ItemModel.find_one(ItemModel.id == ObjectId(id))
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        update_data = item_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(item, field, value)
        
        await item.save()
        return ItemOut(
            id=str(item.id),
            name=item.name,
            price=item.price,
        )
    
    @staticmethod
    async def delete_item(id: str) -> bool:
        item = await ItemModel.find_one(ItemModel.id == ObjectId(id))
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        await item.delete()
        return True

