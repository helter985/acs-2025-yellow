from fastapi import FastAPI
from app.core.config import settings


def create_app():
    # Initialize Flask
    app = FastAPI(title=settings.PROJECT_NAME)


    # Return initialized app
    return app

