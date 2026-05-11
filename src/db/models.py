# SQLite models
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Appointment:
    id: Optional[int]
    user_id: str           # Telegram user_id
    user_name: str
    service: str
    date: str              # YYYY-MM-DD
    time: str              # HH:MM
    notes: Optional[str]
    status: str            # confirmed / cancelled
    created_at: str
    updated_at: str

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "service": self.service,
            "date": self.date,
            "time": self.time,
            "notes": self.notes,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
