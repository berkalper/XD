from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass(frozen=True)
class Visit:
    note: str
    created_at: datetime


@dataclass(frozen=True)
class Appointment:
    scheduled_at: datetime
    note: str


@dataclass
class Patient:
    patient_id: str
    full_name: str
    phone: str
    age: int
    gender: str
    visits: List[Visit] = field(default_factory=list)
    appointments: List[Appointment] = field(default_factory=list)

    def add_visit(self, note: str, created_at: datetime) -> None:
        self.visits.append(Visit(note=note, created_at=created_at))

    def add_appointment(self, scheduled_at: datetime, note: str) -> None:
        self.appointments.append(Appointment(scheduled_at=scheduled_at, note=note))
