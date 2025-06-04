from pydantic import BaseModel
from typing import Optional


class ItemCreate(BaseModel):
    name: str
    price: float
    barcode: str


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    barcode: Optional[str] = None


class ItemOut(BaseModel):
    id: str
    name: str
    price: float
    barcode: str

