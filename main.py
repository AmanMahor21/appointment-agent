import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import httpx

from src.route import register_routes
from src.db.database import db
from src.config import settings

load_dotenv()


async def _register_webhook():
    url = f"{settings.telegram_api_base}/setWebhook"
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(url, json={
            "url": settings.telegram_webhook_url,
            "allowed_updates": ["message"],
            "drop_pending_updates": True,
        })
        response.raise_for_status()
        print(f"Webhook registered → {settings.telegram_webhook_url}")


@asynccontextmanager
async def lifespan(app):
    await db.initialize()
    print("Database initialized")
    await _register_webhook()
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
