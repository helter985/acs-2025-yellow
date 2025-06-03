import pytest
from unittest.mock import Mock, patch, AsyncMock
from app.services.item_service import ItemService
from app.models.item_model import ItemModel
from app.schemas.item_schema import ItemCreate, ItemOut, ItemUpdate
from fastapi import HTTPException
from bson import ObjectId

@pytest.fixture
def mock_item():
    item = Mock()
    item.id = ObjectId()
    item.name = "Coca Cola"
    item.barcode = "1234567890123"
    item.price = 1.99
    return item


@pytest.fixture
def mock_item_out(mock_item):
    return ItemOut(
        id=str(mock_item.id),
        name=mock_item.name,
        barcode=mock_item.barcode,
        price=mock_item.price
    )
