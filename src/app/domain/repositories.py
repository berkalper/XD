from __future__ import annotations

from typing import Iterable, Protocol

from app.domain.entities import Patient


class PatientRepository(Protocol):
    def add(self, patient: Patient) -> None:
        ...

    def list_all(self) -> Iterable[Patient]:
        ...

    def get(self, patient_id: str) -> Patient | None:
        ...

    def save(self, patient: Patient) -> None:
        ...
