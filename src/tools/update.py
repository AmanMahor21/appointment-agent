# Update appointment tool
from langchain_core.tools import tool
from src.db.database import db
from typing import Optional, Union


@tool
async def update_appointment(
    appointment_id: int,
    user_id: Union[str, int],
    service: Optional[str] = None,
    date: Optional[str] = None,
    time: Optional[str] = None,
    notes: Optional[str] = None,
) -> str:
    """
    Update an existing appointment. Only provide fields you want to change.

    Args:
        appointment_id: The ID of the appointment to update (from booking confirmation)
        user_id: Telegram user ID (always pass from context, for security)
        service: New service type (optional)
        date: New date in YYYY-MM-DD format (optional)
        time: New time in HH:MM format (optional)
        notes: New notes (optional)

    Returns:
        Updated appointment details or error message
    """

    if not any([service, date, time, notes]):
        return "Please specify what you want to change (date, time, service, or notes)."

    # If date/time is changing, check new slot availability
    if date or time:
        existing = await db.get_appointment(appointment_id)
        if existing:
            check_date = date or existing.date
            check_time = time or existing.time
            # Only check if the date/time actually changed
            if check_date != existing.date or check_time != existing.time:
                is_available = await db.check_slot_availability(check_date, check_time)
                if not is_available:
                    return (
                        f"Sorry, the slot on {check_date} at {check_time} is already taken. "
                        "Please pick a different time."
                    )

    appointment = await db.update_appointment(
        appointment_id=appointment_id,
        user_id=user_id,
        service=service,
        date=date,
        time=time,
        notes=notes,
    )
    print("Updated appointment from DB:", appointment)
    if not appointment:
        return (
            f"Could not update appointment #{appointment_id}. "
            "It may not exist, be cancelled, or belong to another user."
        )

    return (
        f"✅ Appointment #{appointment.id} updated!\n"
        f"🔧 Service: {appointment.service}\n"
        f"📅 Date: {appointment.date}\n"
        f"🕐 Time: {appointment.time}\n"
        f"📝 Notes: {appointment.notes or 'None'}\n"
        f"Status: {appointment.status.upper()}"
    )
