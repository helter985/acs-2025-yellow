from beanie import Document
from typing import Optional
from pydantic import Field

class ItemModel(Document):
    name: str
    price: int
    
    # Optional fields for Algorand transaction details
    transaction_id_algorand: Optional[str] = None

    def __repr__(self) -> str:
        return f"<Item {self.name}>"

    class Settings:
        name = "items"