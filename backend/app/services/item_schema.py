from pydantic import BaseModel
from typing import Optional


class ItemCreate(BaseModel):
    name: str
    price: int
    transaction_id_algorand: Optional[str] = None


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None
    transaction_id_algorand: Optional[str] = None


class ItemOut(BaseModel):
    id: str
    name: str
    price: int
    transaction_id_algorand: Optional[str] = None