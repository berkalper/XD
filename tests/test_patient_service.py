import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from app.application.use_cases import (
    AddVisitRequest,
    PatientService,
    RegisterPatientRequest,
    ScheduleAppointmentRequest,
)
from app.infrastructure.json_repository import JsonPatientRepository


class TestPatientService(unittest.TestCase):
    def test_patient_service_flow(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = JsonPatientRepository(Path(temp_dir) / "patients.json")
            service = PatientService(repo)

            patient = service.register_patient(
                RegisterPatientRequest(
                    patient_id="P-2",
                    full_name="Grace Hopper",
                    phone="555-0202",
                    age=45,
                    gender="Kadın",
                )
            )
            self.assertEqual(patient.patient_id, "P-2")

            updated = service.add_visit(AddVisitRequest(patient_id="P-2", note="Not"))
            self.assertEqual(len(updated.visits), 1)

            scheduled = service.schedule_appointment(
                ScheduleAppointmentRequest(
                    patient_id="P-2",
                    scheduled_at=datetime(2024, 1, 3, 14, 0),
                    note="Kontrol",
                )
            )
            self.assertEqual(len(scheduled.appointments), 1)


if __name__ == "__main__":
    unittest.main()
