from __future__ import annotations

from pathlib import Path

from app.application.use_cases import PatientService
from app.infrastructure.json_repository import JsonPatientRepository
from app.interface.cli import CliApp


def main() -> None:
    repository = JsonPatientRepository(Path("data/patients.json"))
    service = PatientService(repository)
    app = CliApp(service)
    app.run()


if __name__ == "__main__":
    main()
