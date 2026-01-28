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

## EXE Oluşturma (Windows)

1. Sanal ortam oluşturup bağımlılıkları kurun:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install pyinstaller
```

2. GUI uygulamasını paketleyin:

```bash
pyinstaller --onefile --noconsole --name hasta-kayit --paths src src/app/gui_main.py
```

`dist/hasta-kayit.exe` dosyası oluşur.

## Mimari

- **domain**: Temel iş modelleri (Patient, Visit).
- **application**: Use-case servisleri.
- **infrastructure**: JSON dosya tabanlı repository.
- **interface**: CLI ve GUI akışları.
