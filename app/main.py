from fastapi import FastAPI
from .core.config import settings
from app.routers.auth import auth_router


app = FastAPI(title=settings.TITLE,
              description=settings.DESCRIPTION)


app.include_router(auth_router)
