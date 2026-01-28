import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from app.domain.entities import Appointment, Patient, Visit
from app.infrastructure.json_repository import JsonPatientRepository


class TestJsonRepository(unittest.TestCase):
    def test_repository_persists_patient_data(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "patients.json"
            repo = JsonPatientRepository(path)

            patient = Patient(
                patient_id="P-1",
                full_name="Ada Lovelace",
                phone="555-0101",
                age=37,
                gender="Kadın",
            )
            patient.visits.append(Visit(note="Kontrol", created_at=datetime(2024, 1, 1, 10, 0)))
            patient.appointments.append(
                Appointment(scheduled_at=datetime(2024, 1, 2, 9, 30), note="Randevu")
            )
            repo.add(patient)

            reloaded = JsonPatientRepository(path)
            loaded = reloaded.get("P-1")
            self.assertIsNotNone(loaded)
            assert loaded is not None
            self.assertEqual(loaded.full_name, "Ada Lovelace")
            self.assertEqual(loaded.age, 37)
            self.assertEqual(loaded.gender, "Kadın")
            self.assertEqual(len(loaded.visits), 1)
            self.assertEqual(loaded.visits[0].note, "Kontrol")
            self.assertEqual(len(loaded.appointments), 1)
            self.assertEqual(loaded.appointments[0].note, "Randevu")


if __name__ == "__main__":
    unittest.main()
