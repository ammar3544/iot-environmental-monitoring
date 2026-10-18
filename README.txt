# IoT Asset Monitoring & Cloud Sync Pipeline

Repositori ini berisi studi kasus pengolahan data sensor *Internet of Things* (IoT) untuk manajemen aset dan pemantauan kondisi lingkungan (mengacu pada pembahasan *Asset Management* dan integrasi data *cloud* pada industri modern[cite: 2, 3]).

## Fitur Utama
- **Data Preprocessing & Validation**: Pembersihan pembacaan sensor yang terdistorsi/hilang dari perangkat lapangan.
- **Automated Health Index Attribution**: Pengelompokan status operasional aset (*OPERATIONAL*, *LOW_BATTERY*, *NEEDS_MAINTENANCE*) secara otomatis.
- **Cloud-Ready Data Aggregation**: Rekapitukasi status aset per *node* untuk sinkronisasi terpusat.

## Cara Menjalankan
1. Install dependencies:
   ```bash
   pip install -r requirements.txt