import numpy as np
import pandas as pd
from datetime import datetime

# Konsistensi pembangkitan data acak
np.random.seed(42)

print('=== PIPELINE IoT MONITORING & MANAJEMEN ASET LINGKUNGAN ===')

# ================= ================= =================
# 1. SIMULASI DATA TELEMETRY SENSOR IoT DARI LAPANGAN
# ================= ================= =================
n_samples = 1200
timestamps = pd.date_range(start='2026-10-01', periods=n_samples, freq='h')

asset_ids = ['AST-BNK-001', 'AST-BNK-002', 'AST-BNK-003', 'AST-BNK-004']

raw_telemetry = {
    'timestamp': timestamps,
    'asset_id': np.random.choice(asset_ids, size=n_samples),
    'latitude': np.random.uniform(-3.8000, -3.7800, size=n_samples),
    'longitude': np.random.uniform(102.2600, 102.2800, size=n_samples),
    # Pembacaan sensor kelembapan/vibrasi aset
    'vibration_level': np.random.normal(loc=12.0, scale=4.0, size=n_samples),
    'temperature_c': np.random.normal(loc=31.0, scale=2.5, size=n_samples),
    'battery_pct': np.random.uniform(15.0, 100.0, size=n_samples)
}

df_iot = pd.DataFrame(raw_telemetry)

# Menyisipkan noise/data rusak dari keterbatasan sensor di lapangan
df_iot.loc[df_iot.sample(frac=0.03, random_state=42).index, 'vibration_level'] = -99.0
df_iot.loc[df_iot.sample(frac=0.02, random_state=42).index, 'temperature_c'] = np.nan

print(f'Total Telemetry Received from Field: {len(df_iot)} records')
print(f"Detected Corrupted Data: {df_iot['temperature_c'].isna().sum() + (df_iot['vibration_level'] == -99.0).sum()} items\n")

# ================= ================= =================
# 2. CLEANSING, VALIDATION & ATTRIBUTE AUTOMATION
# ================= ================= =================
# Membersihkan pembacaan sensor yang tidak valid
df_clean = df_iot.copy()
df_clean.loc[df_clean['vibration_level'] < 0, 'vibration_level'] = np.nan
df_clean['vibration_level'] = df_clean['vibration_level'].fillna(df_clean['vibration_level'].median())
df_clean['temperature_c'] = df_clean['temperature_c'].fillna(df_clean['temperature_c'].mean())

# Otomatisasi Atribut Status Aset (Asset Health Index)
def evaluate_asset_health(row):
    if row['vibration_level'] > 18.0 or row['temperature_c'] > 35.0:
        return 'NEEDS_MAINTENANCE'
    elif row['battery_pct'] < 20.0:
        return 'LOW_BATTERY_WARNING'
    else:
        return 'OPERATIONAL'

df_clean['asset_status'] = df_clean.apply(evaluate_asset_health, axis=1)

# ================= ================= =================
# 3. RINGKASAN REKAPITULASI ASET UNTUK CLOUD SYNC
# ================= ================= =================
summary = df_clean.groupby('asset_id').agg(
    last_seen=('timestamp', 'max'),
    avg_temp=('temperature_c', 'mean'),
    max_vibration=('vibration_level', 'max'),
    min_battery=('battery_pct', 'min'),
    critical_alerts=('asset_status', lambda x: (x == 'NEEDS_MAINTENANCE').sum())
).reset_index()

print('--- RINGKASAN STATUS SINKRONISASI ASET (CLOUD DATABASE) ---')
print(summary.to_string(index=False))

# Simpan output bersih siap kirim ke database/API
df_clean.to_csv('processed_asset_telemetry.csv', index=False)
print('\n[SUCCESS] Processed telemetry saved to "processed_asset_telemetry.csv"')