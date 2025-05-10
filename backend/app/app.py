from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import settings
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.models.item_model import ItemModel
from app.api.router import router


# print("MONGO_CONNECTION_STRING: ", settings.MONGO_CONNECTION_STRING)


@asynccontextmanager
async def lifespan(app: FastAPI):
    '''
        initialize crucial app services
    '''
    
    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)
    db = db_client.secuvote

    await init_beanie(
        database=db,
        document_models = [
            ItemModel
        ]
    )
    print("Connected to MongoDB successfully.")
    yield
    db_client.close()


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)


app.include_router(router, prefix=settings.API_V1_STR)

