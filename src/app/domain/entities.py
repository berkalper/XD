from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass(frozen=True)
class Visit:
    note: str
    created_at: datetime


@dataclass
class Patient:
    patient_id: str
    full_name: str
    phone: str
    visits: List[Visit] = field(default_factory=list)

    def add_visit(self, note: str, created_at: datetime) -> None:
        self.visits.append(Visit(note=note, created_at=created_at))
