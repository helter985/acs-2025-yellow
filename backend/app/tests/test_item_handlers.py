import unittest
from unittest.mock import patch
from httpx import AsyncClient, ASGITransport
from fastapi import status
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.item_model import ItemModel
from app.main import app


class TestItemHandlers(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.db_client = AsyncIOMotorClient("mongodb://localhost:27017")
        db = self.db_client["test_database"]
        await init_beanie(database=db, document_models=[ItemModel])
        await db[ItemModel.Settings.name].delete_many({})

        self.transport = ASGITransport(app=app)

    async def asyncTearDown(self):
        self.db_client.close()

    @patch("app.api.handlers.item.ItemService.get_items")
    async def test_get_items(self, mock_get_items):
        fake_items = [
            {"id": "1", "name": "Coca Cola", "price": 1200, "barcode": "7790895001234"},
            {"id": "2", "name": "Pepsi", "price": 1100, "barcode": "7790895005678"}
        ]
        mock_get_items.return_value = fake_items

        async with AsyncClient(transport=self.transport, base_url="http://test") as ac:
            response = await ac.get("/api/v1/items/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]["name"], "Coca Cola")

    @patch("app.api.handlers.item.ItemService.get_item_by_id")
    async def test_get_item_by_id(self, mock_get_item_by_id):
        fake_item = {"id": "1", "name": "Coca Cola", "price": 1200, "barcode": "7790895001234"}
        mock_get_item_by_id.return_value = fake_item

        async with AsyncClient(transport=self.transport, base_url="http://test") as ac:
            response = await ac.get("/api/v1/items/1")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["name"], "Coca Cola")

    @patch("app.api.handlers.item.ItemService.get_item_by_id")
    async def test_get_item_by_id_not_found(self, mock_get_item_by_id):
        mock_get_item_by_id.return_value = None

        async with AsyncClient(transport=self.transport, base_url="http://test") as ac:
            response = await ac.get("/api/v1/items/999")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()["detail"], "Item not found")

    @patch("app.api.handlers.item.ItemService.get_item_by_barcode")
    async def test_get_item_by_barcode(self, mock_get_item_by_barcode):
        fake_item = {"id": "2", "name": "Pepsi", "price": 1100, "barcode": "7790895005678"}
        mock_get_item_by_barcode.return_value = fake_item

        async with AsyncClient(transport=self.transport, base_url="http://test") as ac:
            response = await ac.get("/api/v1/items/barcode/7790895005678")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["name"], "Pepsi")


if __name__ == "__main__":
    unittest.main()
