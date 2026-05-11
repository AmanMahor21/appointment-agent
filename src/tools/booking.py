# Book appointment tool
import asyncio
from langchain_core.tools import tool
from src.db.database import db
from datetime import datetime, time as dt_time, date
from typing import Union


@tool
async def book_appointment(
    user_id: Union[str, int],
    user_name: str,
    service: str,
    date: str,
    time: str,
    notes: str = "",
) -> str:
    """
    Book a new appointment.

    Args:
        user_id: Telegram user ID (always pass the one from context)
        user_name: Full name of the user
        service: Type of service requested (e.g., 'Haircut', 'Consultation')
        date: Appointment date in YYYY-MM-DD format
        time: Appointment time in HH:MM format (24-hour)
        notes: Optional extra notes

    Returns:
        Confirmation message with appointment ID
    """

    try:
        appointment_date = datetime.strptime(date, "%Y-%m-%d").date()
        appointment_time = datetime.strptime(time, "%H:%M").time()
    except ValueError:
        return f"Invalid date or time format. Use YYYY-MM-DD and HH:MM (24-hour)."

    now = datetime.now()
    today = now.date()
    current_time = now.time()

    # Check business hours
    if appointment_time < dt_time(9, 0) or appointment_time > dt_time(18, 0):
        return (
            f"❌ Selected time {time} is outside business hours.\n"
            "Business hours are 09:00 to 18:00 (Monday-Saturday).\n"
            "Please choose a time between 09:00 and 18:00."
        )

    # Check day of week (if you want to block Sundays)
    if appointment_date.weekday() == 6:
        return "❌ We are closed on Sundays. Please choose another day."

    #  No past dates
    if appointment_date < today:
        return f"{date} is in the past.\n" "Please choose a valid future appointment date."

    # If today, time must be in future
    if appointment_date == today and appointment_time < current_time:
        return f"{time} has already passed for today.\n" "Please choose a later time slot."

    # Check slot availability
    is_available = await db.check_slot_availability(date, time)
    if not is_available:
        return (
            f"Sorry, the slot on {date} at {time} is already booked. "
            "Please choose a different date or time."
        )

    appointment = await db.create_appointment(
        user_id=user_id,
        user_name=user_name,
        service=service,
        date=date,
        time=time,
        notes=notes if notes else None,
    )

    return (
        f"✅ Appointment booked successfully!\n"
        f"📋 ID: #{appointment.id}\n"
        f"👤 Name: {appointment.user_name}\n"
        f"🔧 Service: {appointment.service}\n"
        f"📅 Date: {appointment.date}\n"
        f"🕐 Time: {appointment.time}\n"
        f"📝 Notes: {appointment.notes or 'None'}\n"
        f"Status: {appointment.status.upper()}"
    )
