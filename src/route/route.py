import httpx
from src.config import settings
from rich import print
from src.core.http import APIClient

client = APIClient()


async def send_message(chat_id: int | str, text: str) -> dict:
    """Send a message to Telegram user."""
    url = f"{settings.telegram_api_base}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
    }

    response = await client.http(url, method="POST", json=payload)
    return response


async def send_chat_action(chat_id: int | str, action: str = "typing") -> dict:
    """Show typing indicator."""
    url = f"{settings.telegram_api_base}/sendChatAction"
    payload = {"chat_id": chat_id, "action": action}

    response = await client.http(url, method="POST", timeout=10.0, json=payload)
    return response
