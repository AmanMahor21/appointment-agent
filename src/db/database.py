# DB connection & operations

import aiosqlite
import asyncio
from datetime import datetime
from typing import Optional
from src.db.models import Appointment
from src.config import settings
from rich import print


class AppointmentDB:
    def __init__(self):
        self.db_path = settings.database_url

    async def initialize(self):
        """Create tables if they don't exist."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS appointments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    user_name TEXT NOT NULL,
                    service TEXT NOT NULL,
                    date TEXT NOT NULL,
                    time TEXT NOT NULL,
                    notes TEXT,
                    status TEXT NOT NULL DEFAULT 'confirmed',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            await db.commit()

    async def create_appointment(
        self,
        user_id: str,
        user_name: str,
        service: str,
        date: str,
        time: str,
        notes: Optional[str] = None,
    ) -> Appointment:
        now = datetime.now().isoformat()
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                """
                INSERT INTO appointments
                (user_id, user_name, service, date, time,
                 notes, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, 'confirmed', ?, ?)
                """,
                (user_id, user_name, service, date, time, notes, now, now),
            )
            await db.commit()
            appt_id = cursor.lastrowid

        return Appointment(
            id=appt_id,
            user_id=user_id,
            user_name=user_name,
            service=service,
            date=date,
            time=time,
            notes=notes,
            status="confirmed",
            created_at=now,
            updated_at=now,
        )

    async def get_appointment(self, appointment_id: int) -> Optional[Appointment]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT * FROM appointments WHERE id = ?", (appointment_id,)
            )
            row = await cursor.fetchone()
            if not row:
                return None
            return Appointment(**dict(row))

    async def get_active_appointment(self, user_id: int) -> int:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                # "SELECT * FROM appointments WHERE id = ?", (appointment_id,)
                "SELECT COUNT(*) FROM appointments WHERE user_id = ? AND status = 'confirmed'", (
                    user_id,)
            )
            row = await cursor.fetchone()
            return row[0] if row else 0

    async def get_user_appointments(
        self, user_id: str, status: Optional[str] = None
    ) -> list[Appointment]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            if status:
                cursor = await db.execute(
                    "SELECT * FROM appointments WHERE user_id = ? AND status = ? ORDER BY date, time",
                    (user_id, status),
                )
            else:
                cursor = await db.execute(
                    "SELECT * FROM appointments WHERE user_id = ? ORDER BY date, time",
                    (user_id,),
                )
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def check_slot_availability(self, date: str, time: str) -> bool:
        """Returns True if the slot is available."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                """
                SELECT COUNT(*) FROM appointments
                WHERE date = ? AND time = ? AND status = 'confirmed'
                """,
                (date, time),
            )
            count = await cursor.fetchone()
            return count[0] == 0

    async def update_appointment(
        self,
        appointment_id: int,
        user_id: str,
        service: Optional[str] = None,
        date: Optional[str] = None,
        time: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Optional[Appointment]:
        """Only update fields that are provided."""
        appointment = await self.get_appointment(appointment_id)
        if not appointment:
            return None
        # Security: user can only update their own
        if appointment.user_id != str(user_id):
            return None
        if appointment.status == "cancelled":
            print("Cannot update a cancelled appointment.")
            return None

        updated_service = service or appointment.service
        updated_date = date or appointment.date
        updated_time = time or appointment.time
        updated_notes = notes if notes is not None else appointment.notes
        now = datetime.now().isoformat()

        async with aiosqlite.connect(self.db_path) as db:
            print("DEBUG INPUTS:")
            print("appointment_id:", appointment_id, type(appointment_id))
            print("user_id:", user_id, type(user_id))
            print("service:", updated_service)
            print("date:", updated_date)
            print("time:", updated_time)
            cursor = await db.execute(
                """
                UPDATE appointments
                SET service = ?, date = ?, time = ?, notes = ?, updated_at = ?
                WHERE id = ? AND user_id = ?
                """,
                (updated_service, updated_date, updated_time,
                 updated_notes, now, appointment_id, user_id),
            )
            await db.commit()
            print("Rows affected:", cursor.rowcount)

        return await self.get_appointment(appointment_id)

    async def cancel_appointment(
        self, appointment_id: int, user_id: str
    ) -> Optional[Appointment]:
        appointment = await self.get_appointment(appointment_id)
        if not appointment:
            return None
        if appointment.user_id != user_id:
            return None
        if appointment.status == "cancelled":
            return appointment  # already cancelled

        now = datetime.now().isoformat()
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                UPDATE appointments
                SET status = 'cancelled', updated_at = ?
                WHERE id = ? AND user_id = ?
                """,
                (now, appointment_id, user_id),
            )
            await db.commit()

        return await self.get_appointment(appointment_id)


# Singleton
db = AppointmentDB()
