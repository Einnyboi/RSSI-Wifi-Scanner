# Cathrine Sandrina - 535240075
# Fakultas Teknologi Informasi, Teknik Informatika
# Universitas Tarumanagara

# "Analisis Komparasi Algoritma Klasifikasi pada Wi-Fi Fingerprinting untuk Pemetaan Dalam Ruangan" - Projek UAS Machine Learning Kelas A
# Kode pengumpulan data (BSSID dan RSSI) Wi-Fi Fingerprinting untuk pemetaan dalam ruangan menggunakan Python

import subprocess
import re
import time
import pandas as pd
from datetime import datetime
import os

def scan_wifi():
    result = subprocess.run(['netsh', 'wlan', 'show', 'networks', 'mode=bssid'], capture_output=True, text=True) # netsh untuk scan jaringan wifi di windows
    output = result.stdout
    bssid_pattern = re.compile(r'BSSID\s+\d+\s+:\s+([a-fA-F0-9:]+)') # regex untuk mengekstrak BSSID dari output netsh
    signal_pattern = re.compile(r'(?:Signal|Sinyal)\s+:\s+(\d+)%') # regex untuk mengekstrak sinyal dari output netsh
    
    bssids = bssid_pattern.findall(output)
    signals = signal_pattern.findall(output)

    scan_data = {}
    for bssid, signal in zip(bssids, signals): # menggabungkan BSSID dan sinyal menjadi dictionary
        rssi = (int(signal) / 2) - 100
        scan_data[bssid] = rssi
        
    return scan_data

KELAS_LABEL = "R805" # nama ruang kelasnya sebagai label
JUMLAH_SCAN = 300 # frekuensi scan jaringan Wi-Fi yang diinginkan
JEDA_WAKTU = 3 # jeda waktu antar scan dalam detik
NAMA_FILE = "data_R805.csv" # ganti nama_(lokasi) sebagai nama file

print(f"Memulai pengumpulan data untuk label: {KELAS_LABEL}")
print(f"Target: {JUMLAH_SCAN} baris data. Silakan bawa laptop keliling area {KELAS_LABEL}...\n")

all_data = []

for i in range(JUMLAH_SCAN):
    print(f"[{i+1}/{JUMLAH_SCAN}] Scanning jaringan Wi-Fi...")
    data_saat_ini = scan_wifi()
    data_saat_ini['Label'] = KELAS_LABEL
    data_saat_ini['Timestamp'] = datetime.now().strftime("%H:%M:%S")
    
    all_data.append(data_saat_ini)
    time.sleep(JEDA_WAKTU)

df_baru = pd.DataFrame(all_data)

if os.path.exists(NAMA_FILE): # cek apakah file sudah ada, jika ada maka gabungkan data baru dengan data lama
    df_lama = pd.read_csv(NAMA_FILE)
    df_gabungan = pd.concat([df_lama, df_baru], ignore_index=True)
    df_gabungan.fillna(-100, inplace=True)
    df_gabungan.to_csv(NAMA_FILE, index=False)
else: # jika file belum ada, maka buat file baru
    df_baru.fillna(-100, inplace=True)
    df_baru.to_csv(NAMA_FILE, index=False)

print(f"\nSelesai! Data berhasil disimpan di {NAMA_FILE}")