import unittest
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from mongomock_motor import AsyncMongoMockClient

from app.models.item_model import ItemModel

class TestItemModel(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        # Crear un cliente mock de MongoDB
        self.client = AsyncMongoMockClient()
        self.db = self.client["test_database"]
        
        # Inicializar Beanie con la base de datos mock
        await init_beanie(database=self.db, document_models=[ItemModel])

    async def test_item_model_creation(self):
        item = ItemModel(name="Coca Cola 600ml", price=1200, barcode="7790895001234")
        await item.insert()

        found = await ItemModel.find_one(ItemModel.barcode == "7790895001234")

        self.assertIsNotNone(found)
        self.assertEqual(found.name, "Coca Cola 600ml")
        self.assertEqual(found.price, 1200)
        self.assertEqual(found.barcode, "7790895001234")

    async def test_repr_method(self):
        item = ItemModel(name="Galletas Oreo", price=800, barcode="0123456789012")
        expected_repr = "<Item Galletas Oreo>"
        self.assertEqual(repr(item), expected_repr)

if __name__ == "__main__":
    unittest.main()