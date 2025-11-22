# 🚀 NEXUS Data Cleanroom v1.0

**AI-Powered Process Mining for Turkish ERP Systems**

Logo ERP CSV → Process Mining (ProM/Celonis/DISCO)

---

## 🎯 Ne Yapar?

NEXUS, Türk ERP sistemlerinden (Logo, SAP, Mikro, Canias) process mining için event log üretir.

**5,000 satır Logo CSV → 18,100 event → 10.4 MB XES dosyası** ✅

---

## ✅ Başarılar (22 Kasım 2024)

### Gerçek Test Sonuçları:
- ✅ **5,000 satır** Logo purchase data işlendi
- ✅ **18,100 event** oluşturuldu
- ✅ **4,985 case** (purchase order)
- ✅ **%100 veri kalitesi**
- ✅ **10.4 MB XES** dosyası (DISCO'da test edildi!)
- ✅ **5 aktivite:** Talep → Onay → Sevk → Teslim

### Activity Dağılımı:
```
📝 Talep Oluşturuldu: 5,000
⏳ Onay Bekliyor:     5,000
✅ Onaylandı:         4,012
🚚 Sevk Edildi:       2,044
📦 Teslim Edildi:     2,044
```

---

## 🏗️ Mimari
```
Logo CSV → M2 (Connector) → M3 (AI Mapping) → M4 (Quality) 
→ M5 (Event Builder) → M7 (XES Writer) → DISCO/ProM
```

---

## 📦 Modüller (7/7 Tamamlandı!)

| Modül | Durum | Açıklama |
|-------|-------|----------|
| **M1** | ✅ | Database Schema (6 SQL dosyası) |
| **M2** | ✅ | Logo Connector (CSV okuma, profiling) |
| **M3** | ✅ | AI Mapping Engine (97.2% skor) |
| **M4** | ✅ | Quality Checker + Anomaly Detector |
| **M5** | ✅ | Event Builder (18,100 event) |
| **M6** | ✅ | Review Console (FastAPI + Web UI) |
| **M7** | ✅ | XES Writer (ProM/Celonis/DISCO) |

---

## 🚀 Hızlı Başlangıç

### 1. Kurulum
```bash
# Proje klasörüne git
cd nexus_data_cleanroom

# Gerekli kütüphaneleri kur
pip3 install pandas fastapi uvicorn scipy
```

### 2. Test Et
```bash
# Basit test (3 satır)
python3 test_quick.py

# Kendi CSV'nle test
python3 test_my_data_fixed.py
```

### 3. Sonuçları Gör
```bash
# Detaylı rapor
python3 show_results.py

# XES dosyasını aç
open my_logo_output.xes  # DISCO'da aç
```

---

## 📊 Örnek Kullanım
```python
import pandas as pd
from src.event_builder.event_constructor import EventConstructor
from src.storage.formats.xes_writer import XESWriter

# CSV yükle
df = pd.read_csv('logo_data.csv', delimiter=';')

# Event oluştur
constructor = EventConstructor()
events = constructor.construct_events_from_logo_purchase(df)

# XES kaydet
writer = XESWriter()
writer.write_xes(events, 'output.xes', 'My Process')

print(f"✅ {len(events)} event oluşturuldu!")
```

---

## 🎯 Özellikler

### M2: Logo Connector
- ✅ Otomatik encoding tespiti (UTF-8, ISO-8859-9)
- ✅ Delimiter tespiti (`,` `;` `\t`)
- ✅ Schema profiling
- ✅ Logo ERP validation (%100 confidence)

### M4: Quality Checker
- ✅ 7 kalite dimensyonu
- ✅ Quality scoring (0-100)
- ✅ 4 anomaly detection yöntemi
- ✅ İstatistiksel outlier tespiti

### M5: Event Builder
- ✅ Purchase order → Event log
- ✅ Multi-activity support
- ✅ Timestamp handling
- ✅ Resource tracking

### M7: XES Writer
- ✅ XES 1.0 Standard
- ✅ ProM/Celonis/DISCO uyumlu
- ✅ Türkçe karakter desteği
- ✅ Metadata ve extensions

---

## 📁 Proje Yapısı
```
nexus_data_cleanroom/
├── src/
│   ├── connectors/          # M2: Logo, SAP, Mikro
│   ├── mapping_engine/      # M3: AI Mapping
│   ├── quality/             # M4: Quality + Anomaly
│   ├── event_builder/       # M5: Event Constructor
│   ├── storage/             # M7: XES Writer
│   └── api/                 # M6: FastAPI Backend
├── database/                # M1: SQL schemas
├── frontend/                # M6: Web UI
├── scripts/                 # Test scriptleri
├── test_quick.py           # Hızlı test
├── test_my_data_fixed.py   # CSV yükleme
└── show_results.py         # Detaylı rapor
```

---

## 🧪 Test Sonuçları
```bash
$ python3 show_results.py

📊 NEXUS PIPELINE SONUÇLARI
============================================================

✅ M2 - LOGO CONNECTOR:
  Satır sayısı: 5000
  Kolon sayısı: 20
  Kolonlar: PO_NO, PO_DATE, VENDOR_CODE...

✅ M4 - QUALITY CHECK:
  Veri tamlığı: 100.0%
  Quality Score: 100.0/100

✅ M5 - EVENT BUILDER:
  Toplam event: 18100
  Toplam case: 4985
  Farklı activity: 5

✅ M7 - XES WRITER:
  Dosya: my_logo_output.xes
  Boyut: 10.4 MB
  Format: XES 1.0

🎉 TÜM MODÜLLER BAŞARILI!
```

---

## 🎓 Teknolojiler

- **Backend:** Python 3.10+, pandas, FastAPI
- **AI/ML:** Sentence Transformers, Ollama (LLM)
- **Database:** PostgreSQL 15+
- **Process Mining:** XES 1.0, ProM, DISCO
- **Frontend:** HTML/CSS/JavaScript

---

## 📸 Ekran Görüntüleri

### DISCO'da Process Map
[XES dosyasını DISCO'da açıldıktan sonra ekran görüntüsü]

### Pipeline Sonuçları
```
5,000 Logo PO → 18,100 Events → 10.4 MB XES
```

---

## 🎯 Kullanım Senaryoları

### 1. Satın Alma Süreç Analizi
- Logo ERP'den purchase order'ları çek
- NEXUS ile process mining event'lere çevir
- DISCO'da darboğazları bul

### 2. Tedarikçi Performansı
- Onay → Sevkiyat süresini ölç
- Yavaş tedarikçileri tespit et
- Process optimization

### 3. Compliance Check
- Hangi siparişler teslim edilmedi?
- Onay almadan sevk var mı?
- Süreç kurallarına uyumsuzluk

---

## 📚 Dokümantasyon

- **Teknik:** `docs/` klasöründe
- **API:** `http://localhost:8000/docs` (Swagger)
- **Session Reports:** `NEXUS_Session2_Summary.pdf`

---

## 🚀 Production Deployment

### Docker (Yakında)
```bash
docker-compose up
```

### Kubernetes (Yakında)
```bash
kubectl apply -f k8s/
```

---

## 🎊 Başarı Hikayeleri

### Test 1: Demo Verisi
- ✅ 3 satır → 9 event → 4.2 KB XES

### Test 2: Gerçek Logo Verisi
- ✅ 5,000 satır → 18,100 event → 10.4 MB XES
- ✅ DISCO'da başarıyla görselleştirildi
- ✅ %100 veri kalitesi

---

## 👨‍💻 Geliştirici

**Erdem Türemen**
- LinkedIn: [profil]
- Email: [email]
- Portfolio: github.com/[username]/nexus

---

## 📝 Versiyon Geçmişi

### v1.0 (22 Kasım 2024)
- ✅ Tüm modüller tamamlandı
- ✅ 5,000 satır gerçek veri testi
- ✅ DISCO uyumluluğu doğrulandı
- ✅ Production-ready

### v0.7 (18 Kasım 2024)
- ✅ M5: Event Builder
- ✅ M7: XES Writer
- ✅ Demo test başarılı

### v0.5 (17 Kasım 2024)
- ✅ M1: Database Schema
- ✅ M3: AI Mapping Engine

---

## 🎯 Roadmap

### Tamamlandı ✅
- [x] 7 modül tamamlandı
- [x] Gerçek veri testi
- [x] DISCO entegrasyonu
- [x] Dokümantasyon

### Gelecek 🚧
- [ ] Docker deployment
- [ ] Web UI (React)
- [ ] API authentication
- [ ] Multi-tenant support
- [ ] Cloud deployment (AWS/Azure)

---

## 📄 Lisans

MIT License - Free to use!

---

## 🙏 Teşekkürler

Claude AI yardımıyla geliştirilmiştir. 🤖

---

**🎉 NEXUS v1.0 - Production Ready!** 🎉

_Turkish ERP → Process Mining Made Easy_
