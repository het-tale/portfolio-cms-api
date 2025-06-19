from fastapi import FastAPI
from .core.config import settings
from app.routers.main import api_router


app = FastAPI(title=settings.TITLE,
              description=settings.DESCRIPTION)


app.include_router(api_router)
