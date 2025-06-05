import unittest
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from bson import ObjectId

from app.models.item_model import ItemModel
from app.services.item_service import ItemService
from app.schemas.item_schema import ItemCreate, ItemOut

class TestItemService(unittest.IsolatedAsyncioTestCase):
    TEST_ITEM = {
        "name": "Coca Cola",
        "barcode": "1234567890123",
        "price": 1.99
    }

    async def asyncSetUp(self):
        print("\n=== Iniciando pruebas de ItemService ===")
        self.client = AsyncIOMotorClient("mongodb://localhost:27017")
        self.db = self.client["test_database"]
        await init_beanie(database=self.db, document_models=[ItemModel])
        await self.db[ItemModel.Settings.name].delete_many({})

    async def asyncTearDown(self):
        await self.db[ItemModel.Settings.name].delete_many({})
        self.client.close()
        print("=== Pruebas finalizadas ===\n")

    async def test_create_item(self):
        print("Probando: Crear nuevo item")
        item_data = ItemCreate(**self.TEST_ITEM)
        result = await ItemService.create_item(item_data)
        
        self.assertEqual(result.name, self.TEST_ITEM["name"])
        self.assertEqual(result.barcode, self.TEST_ITEM["barcode"])
        self.assertEqual(result.price, self.TEST_ITEM["price"])
        print(f"Item creado: {result.name}")
        
        saved_item = await ItemModel.find_one(ItemModel.barcode == self.TEST_ITEM["barcode"])
        self.assertIsNotNone(saved_item)

    async def test_get_item_by_id(self):
        print("Probando: Obtener item por ID")
        test_item = ItemModel(**self.TEST_ITEM)
        await test_item.insert()
        
        result = await ItemService.get_item_by_id(str(test_item.id))
        self.assertEqual(result.name, self.TEST_ITEM["name"])
        print(f"Item encontrado: {result.name}")

    async def test_get_item_by_barcode(self):
        print("Probando: Obtener item por código de barras")
        test_item = ItemModel(**self.TEST_ITEM)
        await test_item.insert()
        
        result = await ItemService.get_item_by_barcode(test_item.barcode)
        self.assertEqual(result.name, self.TEST_ITEM["name"])
        print(f"Item encontrado: {result.name}")

    async def test_get_items(self):
        print("Probando: Listar todos los items")
        test_items = [
            ItemModel(name="Coca Cola", barcode="1234567890123", price=1.99),
            ItemModel(name="Pepsi", barcode="9876543210987", price=1.89)
        ]
        
        for item in test_items:
            await item.insert()

        results = await ItemService.get_items()
        self.assertEqual(len(results), len(test_items))
        print(f"Items encontrados: {len(results)}")

    async def test_get_nonexistent_item(self):
        print("Probando: Buscar item inexistente")
        test_id = str(ObjectId())
        with self.assertRaises(Exception) as context:
            await ItemService.get_item_by_id(test_id)
        self.assertEqual(context.exception.status_code, 404)
        print("Error manejado correctamente")

if __name__ == "__main__":
    unittest.main()
