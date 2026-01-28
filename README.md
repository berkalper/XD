# Hasta Kayıt Sistemi (CLI + GUI)

Bu proje doktor ve sekreter için basit bir hasta kayıt sistemi sunar. Temiz mimariyi takip eden
küçük bir komut satırı (CLI) ve masaüstü (Tkinter GUI) uygulamasıdır.

## Çalıştırma

CLI:

```bash
PYTHONPATH=src python -m app.main
```

GUI:

```bash
PYTHONPATH=src python -m app.gui_main
```

Uygulama hasta kayıtlarını `data/patients.json` dosyasında saklar.

## Tek Tıkla Açılabilir .exe (Windows)

Windows üzerinde aşağıdaki PowerShell betiği `.exe` üretir:

```powershell
./scripts/build_exe.ps1
```

Üretim tamamlandıktan sonra `dist/hasta-kayit.exe` dosyasını çift tıklayarak uygulamayı
başlatabilirsiniz. Veri dosyası `.exe` ile aynı klasörün altındaki `data/patients.json` içinde
oluşturulur.

Manuel adımlar isterseniz:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install pyinstaller
pyinstaller --onefile --noconsole --name hasta-kayit --paths src src/app/gui_main.py
```

`dist/hasta-kayit.exe` dosyası oluşur.

> Not: `.exe` üretimi Windows ortamı gerektirir. Linux/macOS üzerinde PyInstaller yerel binary
> üretir, `.exe` değil.

## Mimari

- **domain**: Temel iş modelleri (Patient, Visit).
- **application**: Use-case servisleri.
- **infrastructure**: JSON dosya tabanlı repository.
- **interface**: CLI ve GUI akışları.
