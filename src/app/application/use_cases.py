from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

from app.domain.entities import Patient
from app.domain.repositories import PatientRepository


@dataclass
class RegisterPatientRequest:
    patient_id: str
    full_name: str
    phone: str
    age: int
    gender: str


@dataclass
class AddVisitRequest:
    patient_id: str
    note: str


@dataclass
class ScheduleAppointmentRequest:
    patient_id: str
    scheduled_at: datetime
    note: str


class PatientService:
    def __init__(self, repository: PatientRepository) -> None:
        self._repository = repository

    def register_patient(self, request: RegisterPatientRequest) -> Patient:
        existing = self._repository.get(request.patient_id)
        if existing is not None:
            raise ValueError("Bu hasta numarası zaten kayıtlı.")
        patient = Patient(
            patient_id=request.patient_id,
            full_name=request.full_name,
            phone=request.phone,
            age=request.age,
            gender=request.gender,
        )
        self._repository.add(patient)
        return patient

    def list_patients(self) -> Iterable[Patient]:
        return self._repository.list_all()

    def add_visit(self, request: AddVisitRequest) -> Patient:
        patient = self._repository.get(request.patient_id)
        if patient is None:
            raise ValueError("Hasta bulunamadı.")
        patient.add_visit(note=request.note, created_at=datetime.utcnow())
        self._repository.save(patient)
        return patient

    def schedule_appointment(self, request: ScheduleAppointmentRequest) -> Patient:
        patient = self._repository.get(request.patient_id)
        if patient is None:
            raise ValueError("Hasta bulunamadı.")
        patient.add_appointment(scheduled_at=request.scheduled_at, note=request.note)
        self._repository.save(patient)
        return patient
