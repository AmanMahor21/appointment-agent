import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import httpx

from src.route import register_routes
from src.route.route import register_webhook
from src.db.database import db
from src.config import settings

load_dotenv()


@asynccontextmanager
async def lifespan(app):
    await db.initialize()
    print("Database initialized")
    await register_webhook()
    yield
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

register_routes(app)


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
