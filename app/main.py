from fastapi import FastAPI
from .core.config import settings
from app.routers.main import api_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title=settings.TITLE, description=settings.DESCRIPTION)


app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
