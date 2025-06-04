import unittest
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from bson import ObjectId

from app.models.item_model import ItemModel
from app.services.item_service import ItemService
from app.schemas.item_schema import ItemCreate, ItemOut

class TestItemService(unittest.IsolatedAsyncioTestCase):
    # Datos de prueba comunes
    TEST_ITEM = {
        "name": "Coca Cola",
        "barcode": "1234567890123",
        "price": 1.99
    }

    async def asyncSetUp(self):
        print("\n=== Configurando el entorno de prueba ===")
        self.client = AsyncIOMotorClient("mongodb://localhost:27017")
        self.db = self.client["test_database"]
        await init_beanie(database=self.db, document_models=[ItemModel])
        await self.db[ItemModel.Settings.name].delete_many({})
        print("Base de datos de prueba inicializada y limpiada")

    async def asyncTearDown(self):
        print("\n=== Limpiando después de la prueba ===")
        await self.db[ItemModel.Settings.name].delete_many({})
        self.client.close()
        print("Base de datos limpiada y conexión cerrada")

    def print_item_details(self, item, prefix=""):
        """Función auxiliar para imprimir detalles del item"""
        print(f"{prefix}Item:")
        print(f"  - Nombre: {item.name}")
        print(f"  - Barcode: {item.barcode}")
        print(f"  - Precio: ${item.price}")

    async def create_test_item(self):
        """Función auxiliar para crear un item de prueba"""
        item = ItemModel(**self.TEST_ITEM)
        await item.insert()
        return item

    async def test_create_item(self):
        print("\n=== Ejecutando test_create_item ===")
        item_data = ItemCreate(**self.TEST_ITEM)
        self.print_item_details(item_data, "Intentando crear ")
        
        result = await ItemService.create_item(item_data)
        self.print_item_details(result, "Item creado exitosamente ")
        
        # Verificaciones
        self.assertIsInstance(result, ItemOut)
        self.assertEqual(result.name, self.TEST_ITEM["name"])
        self.assertEqual(result.barcode, self.TEST_ITEM["barcode"])
        self.assertEqual(result.price, self.TEST_ITEM["price"])
        
        saved_item = await ItemModel.find_one(ItemModel.barcode == self.TEST_ITEM["barcode"])
        self.assertIsNotNone(saved_item)
        self.assertEqual(saved_item.name, self.TEST_ITEM["name"])
        print("Todas las verificaciones completadas")

    async def test_get_item_by_id(self):
        print("\n=== Ejecutando test_get_item_by_id ===")
        test_item = await self.create_test_item()
        print(f"Item de prueba creado con ID: {test_item.id}")

        result = await ItemService.get_item_by_id(str(test_item.id))
        self.print_item_details(result, "Item recuperado ")
        
        # Verificaciones
        self.assertIsInstance(result, ItemOut)
        self.assertEqual(result.name, self.TEST_ITEM["name"])
        self.assertEqual(result.barcode, self.TEST_ITEM["barcode"])
        self.assertEqual(result.price, self.TEST_ITEM["price"])
        print("Todas las verificaciones completadas")

    async def test_get_item_by_barcode(self):
        print("\n=== Ejecutando test_get_item_by_barcode ===")
        test_item = await self.create_test_item()
        print(f"Buscando item por barcode: {test_item.barcode}")

        result = await ItemService.get_item_by_barcode(test_item.barcode)
        self.print_item_details(result, "Item encontrado ")
        
        # Verificaciones
        self.assertIsInstance(result, ItemOut)
        self.assertEqual(result.name, self.TEST_ITEM["name"])
        self.assertEqual(result.barcode, self.TEST_ITEM["barcode"])
        self.assertEqual(result.price, self.TEST_ITEM["price"])
        print("Todas las verificaciones completadas")

    async def test_get_items(self):
        print("\n=== Ejecutando test_get_items ===")
        test_items = [
            ItemModel(name="Coca Cola", barcode="1234567890123", price=1.99),
            ItemModel(name="Pepsi", barcode="9876543210987", price=1.89),
            ItemModel(name="Sprite", barcode="4567891234567", price=1.79)
        ]
        
        for item in test_items:
            await item.insert()
        print(f"Se crearon {len(test_items)} items de prueba")

        results = await ItemService.get_items()
        print(f"Se recuperaron {len(results)} items")
        
        # Verificaciones
        self.assertEqual(len(results), len(test_items))
        self.assertTrue(all(isinstance(item, ItemOut) for item in results))
        for item in test_items:
            self.assertTrue(any(r.name == item.name for r in results))
        print("Todas las verificaciones completadas")

    async def test_get_nonexistent_item(self):
        print("\n=== Ejecutando test_get_nonexistent_item ===")
        test_id = str(ObjectId())
        print(f"Intentando obtener item con ID inexistente: {test_id}")
        
        with self.assertRaises(Exception) as context:
            await ItemService.get_item_by_id(test_id)

        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, "Item not found")
        print("Se verificó correctamente el manejo del error")

if __name__ == "__main__":
    unittest.main()
