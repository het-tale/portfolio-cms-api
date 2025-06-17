from fastapi import FastAPI
from .core.config import settings
from contextlib import asynccontextmanager
from .core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("server is starting")
    await init_db()
    yield
    print("server is being stopped")

app = FastAPI(title=settings.TITLE,
              description=settings.DESCRIPTION, lifespan=lifespan)


@app.get("/")
def say_hello():
    return "Hello, World!"
