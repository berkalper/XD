from __future__ import annotations

from app.application.use_cases import PatientService
from app.config import get_data_path
from app.infrastructure.json_repository import JsonPatientRepository
from app.interface.gui import GuiApp


def main() -> None:
    repository = JsonPatientRepository(get_data_path())
    service = PatientService(repository)
    app = GuiApp(service)
    app.run()


if __name__ == "__main__":
    main()
