# Hasta Kayıt Sistemi (CLI)

Bu proje doktor ve sekreter için basit bir hasta kayıt sistemi sunar. Temiz mimariyi takip eden
küçük bir komut satırı uygulamasıdır.

## Çalıştırma

```bash
PYTHONPATH=src python -m app.main
```

Uygulama hasta kayıtlarını `data/patients.json` dosyasında saklar.

## Mimari

- **domain**: Temel iş modelleri (Patient, Visit).
- **application**: Use-case servisleri.
- **infrastructure**: JSON dosya tabanlı repository.
- **interface**: CLI akışları.
