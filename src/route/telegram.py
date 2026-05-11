

from fastapi import APIRouter, Request, status
from pydantic import BaseModel
from typing import Optional
from langchain_core.messages import HumanMessage

from src.agent import appointment_graph
from src.route.route import send_message, send_chat_action
from rich import print
router = APIRouter()


@router.post("/webhook/telegram")
async def telegram_webhook(request: Request):
    data = await request.json()
    # print(data, 'req data from telegram')

    message = data.get("message") or {}
    text = message.get("text")
    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    from_user = message.get("from") or {}

    if not chat_id or not text:
        return {"status": "ignored"}

    user_id = str(chat_id)
    user_name = from_user.get("first_name", "")
    last_name = from_user.get("last_name", "")
    if last_name:
        user_name = f"{user_name} {last_name}".strip()
    user_name = user_name or "User"

    if text.startswith("/start"):
        await send_message(
            chat_id,
            f"👋 Hello *{user_name}*! I'm your appointment booking assistant.\n\n"
            "I can help you:\n"
            "📌 Book a new appointment\n"
            "✏️ Update an existing appointment\n"
            "❌ Cancel an appointment\n"
            "📋 View your appointments\n\n"
            "Just tell me what you'd like to do!",
        )
        return {"status": "ok"}

    if text.startswith("/help"):
        await send_message(
            chat_id,
            "🤖 *Appointment Bot Help*\n\n"
            "Just chat naturally! You can say things like:\n"
            "• 'Book me a haircut for tomorrow at 2pm'\n"
            "• 'Change my appointment #3 to Friday'\n"
            "• 'Cancel appointment #5'\n"
            "• 'Show my upcoming appointments'",
        )
        return {"status": "ok"}

    await send_chat_action(chat_id, "typing")

    thread_config = {"configurable": {"thread_id": f"telegram_{user_id}"}}

    try:
        result = await appointment_graph.ainvoke(
            {
                "messages": [HumanMessage(content=text)],
                "user_id": user_id,
                "user_name": user_name,
            },
            config=thread_config,
        )
        # print('graph result', result, 'graph result')

        response_text = result["messages"][-1].content
        await send_message(
            chat_id,
            response_text or "⚠️ Got an empty response. Please try again.",
        )

    except Exception as e:
        await send_message(chat_id, "⚠️ Something went wrong. Please try again.")
        raise e

    return {"status": "ok"}
