from beanie import Document
from typing import Optional
from pydantic import Field

class ItemModel(Document):
    name: str
    price: int
    barcode: str

    def __repr__(self) -> str:
        return f"<Item {self.name}>"

    class Settings:
        name = "items"

