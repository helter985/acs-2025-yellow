import pytest
from unittest.mock import AsyncMock, patch
from bson import ObjectId
from app.services.item_service import ItemService
from app.schemas.item_schema import ItemOut

@pytest.mark.asyncio
async def test_get_item_by_id_returns_item(mock_item):
    test_id = str(mock_item.id)

    with patch("app.models.item_model.ItemModel.find_one", new=AsyncMock(return_value=mock_item)):
        item_out = await ItemService.get_item_by_id(test_id)

    assert isinstance(item_out, ItemOut)
    assert item_out.id == test_id
    assert item_out.name == mock_item.name
    assert item_out.barcode == mock_item.barcode
    assert item_out.price == mock_item.price
