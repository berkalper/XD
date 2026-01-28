$ErrorActionPreference = "Stop"

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install pyinstaller

pyinstaller --onefile --noconsole --name hasta-kayit --paths src src/app/gui_main.py

Write-Host "EXE created at dist/hasta-kayit.exe"
