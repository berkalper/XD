from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable

from app.domain.entities import Patient, Visit
from app.domain.repositories import PatientRepository


class JsonPatientRepository(PatientRepository):
    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path
        self._patients: Dict[str, Patient] = {}
        self._load()

    def add(self, patient: Patient) -> None:
        self._patients[patient.patient_id] = patient
        self._persist()

    def list_all(self) -> Iterable[Patient]:
        return sorted(self._patients.values(), key=lambda item: item.full_name.lower())

    def get(self, patient_id: str) -> Patient | None:
        return self._patients.get(patient_id)

    def save(self, patient: Patient) -> None:
        self._patients[patient.patient_id] = patient
        self._persist()

    def _load(self) -> None:
        if not self._file_path.exists():
            self._file_path.parent.mkdir(parents=True, exist_ok=True)
            self._file_path.write_text("[]", encoding="utf-8")
            return
        raw = self._file_path.read_text(encoding="utf-8")
        data = json.loads(raw or "[]")
        self._patients = {item["patient_id"]: self._deserialize_patient(item) for item in data}

    def _persist(self) -> None:
        payload = [self._serialize_patient(patient) for patient in self._patients.values()]
        self._file_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    @staticmethod
    def _serialize_patient(patient: Patient) -> dict:
        return {
            "patient_id": patient.patient_id,
            "full_name": patient.full_name,
            "phone": patient.phone,
            "visits": [
                {"note": visit.note, "created_at": visit.created_at.isoformat()}
                for visit in patient.visits
            ],
        }

    @staticmethod
    def _deserialize_patient(payload: dict) -> Patient:
        visits = [
            Visit(note=item["note"], created_at=datetime.fromisoformat(item["created_at"]))
            for item in payload.get("visits", [])
        ]
        return Patient(
            patient_id=payload["patient_id"],
            full_name=payload["full_name"],
            phone=payload["phone"],
            visits=visits,
        )
