import unittest
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from pymongo.errors import ConnectionFailure
import os
from app.models.item_model import ItemModel


class TestDatabase(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.mongo_url = ("mongodb://localhost:27017")
        self.db_name = "test_database"
        
        try:
            self.client = AsyncIOMotorClient(self.mongo_url)
            self.db = self.client[self.db_name]
            # Verify connection
            await self.client.admin.command('ping')
        except ConnectionFailure:
            self.fail("Failed to connect to MongoDB")

    async def asyncTearDown(self):
        # Clean up database after tests
        if hasattr(self, 'client'):
            await self.db.command("dropDatabase")
            self.client.close()

    async def test_database_connection(self):
        # Test database connection
        try:
            await self.client.admin.command('ping')
            self.assertTrue(True)
        except ConnectionFailure:
            self.fail("Failed to connect to database")

    async def test_beanie_initialization(self):
        try:
            await init_beanie(
                database=self.db,
                document_models=[ItemModel]
            )
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Beanie initialization failed: {str(e)}")

    async def test_database_operations(self):
        await init_beanie(database=self.db, document_models=[ItemModel])
        
        # Test CREATE
        test_item = ItemModel(name="Test Item", price=100, barcode="1234567890123")
        await test_item.insert()
        
        # Test READ
        found_item = await ItemModel.find_one(ItemModel.barcode == "1234567890123")
        self.assertIsNotNone(found_item)
        self.assertEqual(found_item.name, "Test Item")
        
        # Test UPDATE
        found_item.price = 200
        await found_item.save()
        updated_item = await ItemModel.find_one(ItemModel.barcode == "1234567890123")
        self.assertEqual(updated_item.price, 200)
        
        # Test DELETE
        await found_item.delete()
        deleted_item = await ItemModel.find_one(ItemModel.barcode == "1234567890123")
        self.assertIsNone(deleted_item)

    async def test_invalid_connection(self):
        # Test invalid connection
        with self.assertRaises(Exception):
            invalid_client = AsyncIOMotorClient(
                "mongodb://invalid:27017",
                serverSelectionTimeoutMS=500
            )
            await invalid_client.admin.command('ping')

if __name__ == "__main__":
    unittest.main()
