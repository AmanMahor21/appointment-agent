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
    # async with httpx.AsyncClient() as client:
    #     response = await client.post(url, json=payload)
    #     response.raise_for_status()
    print(response, 'ressssssssssssssssssssssss')
    return response


async def send_chat_action(chat_id: int | str, action: str = "typing") -> dict:
    """Show typing indicator."""
    url = f"{settings.telegram_api_base}/sendChatAction"
    payload = {"chat_id": chat_id, "action": action}
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        return response.json()
