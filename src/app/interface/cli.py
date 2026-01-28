from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from app.application.use_cases import (
    AddVisitRequest,
    PatientService,
    RegisterPatientRequest,
)


@dataclass
class MenuItem:
    key: str
    label: str
    action: Callable[[], None]


class CliApp:
    def __init__(self, service: PatientService) -> None:
        self._service = service
        self._menu = [
            MenuItem("1", "Sekreter: Hasta kaydı oluştur", self._register_patient),
            MenuItem("2", "Doktor: Hasta listesi", self._list_patients),
            MenuItem("3", "Doktor: Muayene notu ekle", self._add_visit),
            MenuItem("0", "Çıkış", self._exit),
        ]
        self._running = True

    def run(self) -> None:
        print("Hasta Kayıt Sistemi")
        while self._running:
            print("\nMenü:")
            for item in self._menu:
                print(f"  {item.key}. {item.label}")
            choice = input("Seçiminiz: ").strip()
            matched = next((item for item in self._menu if item.key == choice), None)
            if matched:
                matched.action()
            else:
                print("Geçersiz seçim. Tekrar deneyin.")

    def _register_patient(self) -> None:
        print("\nHasta Kaydı")
        patient_id = input("Hasta numarası: ").strip()
        full_name = input("Ad Soyad: ").strip()
        phone = input("Telefon: ").strip()
        try:
            patient = self._service.register_patient(
                RegisterPatientRequest(
                    patient_id=patient_id,
                    full_name=full_name,
                    phone=phone,
                )
            )
        except ValueError as exc:
            print(f"Hata: {exc}")
            return
        print(f"Kayıt tamamlandı: {patient.full_name}")

    def _list_patients(self) -> None:
        print("\nHasta Listesi")
        patients = list(self._service.list_patients())
        if not patients:
            print("Henüz kayıt yok.")
            return
        for patient in patients:
            print(
                f"- {patient.patient_id} | {patient.full_name} | {patient.phone} | "
                f"Muayene: {len(patient.visits)}"
            )

    def _add_visit(self) -> None:
        print("\nMuayene Notu Ekle")
        patient_id = input("Hasta numarası: ").strip()
        note = input("Not: ").strip()
        try:
            patient = self._service.add_visit(AddVisitRequest(patient_id=patient_id, note=note))
        except ValueError as exc:
            print(f"Hata: {exc}")
            return
        print(f"Not eklendi. Toplam muayene: {len(patient.visits)}")

    def _exit(self) -> None:
        print("Çıkılıyor...")
        self._running = False
