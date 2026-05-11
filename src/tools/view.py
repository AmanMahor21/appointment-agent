from langchain_core.tools import tool
from src.db.database import db
from typing import Optional, Union
from rich import print


@tool
async def view_appointments(user_id: Union[str, int], status: Optional[str] = None) -> str:
    """
    View all appointments for the current user.

    Args:
        user_id: Telegram user ID (always pass from context)
        status: Filter by status - 'confirmed' or 'cancelled' (optional, returns all if not provided)

    Returns:
        List of appointments or a message if none found
    """
    appointments = await db.get_user_appointments(user_id=user_id, status=status)

    if not appointments:
        filter_msg = f" with status '{status}'" if status else ""
        return f"You have no appointments{filter_msg}."

    lines = [
        f"Appointments found: {len(appointments)}",
        ""
    ]

    for appt in appointments:
        lines.extend(
            [
                f"Appointment ID: {appt['id']}",
                f"Service: {appt['service']}",
                f"Date: {appt['date']}",
                f"Time: {appt['time']}",
                f"Status: {appt['status']}",
                f"Notes: {appt['notes'] or 'None'}",
                "",
            ]
        )

    return "\n".join(lines)
