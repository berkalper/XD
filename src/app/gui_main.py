from __future__ import annotations

from pathlib import Path

from app.application.use_cases import PatientService
from app.infrastructure.json_repository import JsonPatientRepository
from app.interface.gui import GuiApp


def main() -> None:
    repository = JsonPatientRepository(Path("data/patients.json"))
    service = PatientService(repository)
    app = GuiApp(service)
    app.run()


if __name__ == "__main__":
    main()
