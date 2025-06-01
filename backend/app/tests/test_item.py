import pytest
from fastapi.testclient import TestClient
from app.app import app
from app.schemas.item_schema import ItemCreate