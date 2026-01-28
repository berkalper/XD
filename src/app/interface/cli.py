from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Callable

from app.application.use_cases import (
    AddVisitRequest,
    PatientService,
    RegisterPatientRequest,
    ScheduleAppointmentRequest,
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
            MenuItem("4", "Doktor: Muayene notlarını görüntüle", self._show_visits),
            MenuItem("5", "Sekreter: Randevu oluştur", self._schedule_appointment),
            MenuItem("6", "Doktor: Randevu listesini görüntüle", self._show_appointments),
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
        age = input("Yaş: ").strip()
        gender = input("Cinsiyet: ").strip()
        if not age.isdigit():
            print("Hata: Yaş sayısal olmalı.")
            return
        try:
            patient = self._service.register_patient(
                RegisterPatientRequest(
                    patient_id=patient_id,
                    full_name=full_name,
                    phone=phone,
                    age=int(age),
                    gender=gender or "Belirtilmedi",
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
                f"Yaş: {patient.age} | Cinsiyet: {patient.gender} | "
                f"Muayene: {len(patient.visits)} | Randevu: {len(patient.appointments)}"
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

    def _show_visits(self) -> None:
        print("\nMuayene Notları")
        patient_id = input("Hasta numarası: ").strip()
        patient = self._service.list_patients()
        selected = next((item for item in patient if item.patient_id == patient_id), None)
        if selected is None:
            print("Hasta bulunamadı.")
            return
        if not selected.visits:
            print("Muayene notu bulunamadı.")
            return
        for visit in selected.visits:
            timestamp = visit.created_at.strftime("%Y-%m-%d %H:%M")
            print(f"- [{timestamp}] {visit.note}")

    def _schedule_appointment(self) -> None:
        print("\nRandevu Oluştur")
        patient_id = input("Hasta numarası: ").strip()
        scheduled_at = input("Tarih Saat (YYYY-AA-GG SS:DD): ").strip()
        note = input("Not (opsiyonel): ").strip()
        try:
            scheduled_dt = datetime.strptime(scheduled_at, "%Y-%m-%d %H:%M")
        except ValueError:
            print("Hata: Tarih formatı geçersiz.")
            return
        try:
            patient = self._service.schedule_appointment(
                ScheduleAppointmentRequest(
                    patient_id=patient_id,
                    scheduled_at=scheduled_dt,
                    note=note,
                )
            )
        except ValueError as exc:
            print(f"Hata: {exc}")
            return
        print(f"Randevu eklendi. Toplam randevu: {len(patient.appointments)}")

    def _show_appointments(self) -> None:
        print("\nRandevu Listesi")
        patient_id = input("Hasta numarası: ").strip()
        patient = self._service.list_patients()
        selected = next((item for item in patient if item.patient_id == patient_id), None)
        if selected is None:
            print("Hasta bulunamadı.")
            return
        if not selected.appointments:
            print("Randevu bulunamadı.")
            return
        for appointment in sorted(selected.appointments, key=lambda item: item.scheduled_at):
            timestamp = appointment.scheduled_at.strftime("%Y-%m-%d %H:%M")
            note = appointment.note or "-"
            print(f"- [{timestamp}] {note}")

    def _exit(self) -> None:
        print("Çıkılıyor...")
        self._running = False
