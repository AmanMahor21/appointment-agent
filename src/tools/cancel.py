# Cancel appointment tool
from langchain_core.tools import tool
from src.db.database import db


@tool
async def cancel_appointment(appointment_id: int, user_id: str) -> str:
    """
    Cancel an existing appointment.

    Args:
        appointment_id: The ID of the appointment to cancel
        user_id: Telegram user ID (always pass from context, for security)

    Returns:
        Cancellation confirmation or error message
    """
    appointment = await db.cancel_appointment(
        appointment_id=appointment_id,
        user_id=user_id,
    )

    if not appointment:
        return (
            f"Could not cancel appointment #{appointment_id}. "
            "It may not exist or belong to another user."
        )

    return (
        f"❌ Appointment #{appointment.id} has been cancelled.\n"
        f"🔧 Service: {appointment.service}\n"
        f"📅 Date: {appointment.date}\n"
        f"🕐 Time: {appointment.time}\n"
        f"Status: CANCELLED"
    )
