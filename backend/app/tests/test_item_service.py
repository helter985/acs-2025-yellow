import pytest
from unittest.mock import Mock, patch, AsyncMock
from app.services.item_service import ItemService
from app.models.item_model import ItemModel
from app.schemas.item_schema import ItemCreate, ItemOut, ItemUpdate
from fastapi import HTTPException
from bson import ObjectId

