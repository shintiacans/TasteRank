# 🍓 YumRank — DSS Pemilihan Tempat Makan (Metode TOPSIS)

Aplikasi Sistem Pendukung Keputusan (DSS) untuk merangking **35 alternatif tempat makan**
berdasarkan **7 kriteria** (kombinasi benefit & cost) menggunakan metode **TOPSIS**.

## 📁 Struktur Proyek (Arsitektur 3-Tier)

```
dss_app/
├── app.py                      # UI Layer (Streamlit) - tampilan & interaksi
├── modules/
│   ├── data_handler.py         # Data Layer - load, validasi, siapkan data
│   ├── topsis.py                # Logic Layer - algoritma TOPSIS murni
│   └── excel_export.py         # Export Layer - hasil ranking ke Excel (.xlsx)
├── tests/
│   └── test_topsis.py          # Unit test & edge case test
├── data/
│   └── tempat_makan.csv        # Dataset (35 alternatif x 7 kriteria)
├── requirements.txt
└── README.md
```

## 🎯 Domain & Kriteria

**Alternatif:** 35 tempat makan (warung, kedai, cafe, resto, dsb — data dummy realistis)

**Kriteria (7):**
| Kriteria | Jenis | Bobot Default |
|---|---|---|
| 💰 Harga Rata-rata/Porsi (Rp) | Cost | 20% |
| 😋 Rasa (1-10) | Benefit | 20% |
| 📍 Jarak (km) | Cost | 15% |
| ✨ Kebersihan (1-10) | Benefit | 15% |
| ⭐ Rating Online (1-5) | Benefit | 15% |
| ⏱️ Waktu Tunggu (menit) | Cost | 10% |
| 🍽️ Variasi Menu (1-10) | Benefit | 5% |

## 🚀 Cara Menjalankan

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Jalankan aplikasi
```bash
streamlit run app.py
```

### 3. Buka browser
Aplikasi otomatis terbuka di `http://localhost:8501`

## 🎚️ Fitur What-If

Geser slider bobot kriteria di sidebar — ranking akan **otomatis update secara real-time**.
Total bobot harus selalu 100%, sistem akan memberi peringatan jika tidak.

## 🧪 Menjalankan Unit Test

```bash
python -m tests.test_topsis
# atau
pytest tests/test_topsis.py -v
```

Mencakup:
1. **Test normal** — perhitungan TOPSIS standar
2. **Edge case 1** — total bobot ≠ 100% → harus ditolak dengan error jelas
3. **Edge case 2** — semua alternatif punya nilai identik → tidak boleh crash/NaN
4. **Edge case 3 (bonus)** — kolom kriteria bernilai 0 semua → tidak boleh crash/NaN

## 📤 Upload Dataset Sendiri

Format CSV wajib memiliki kolom:
`ID, Nama_Tempat_Makan, Harga_Rata2_Porsi, Rasa, Jarak_km, Kebersihan, Rating_Online, Waktu_Tunggu_menit, Variasi_Menu`

## 📥 Export Hasil (Excel)

Hasil ranking dapat diunduh langsung dalam format **Excel (.xlsx)** melalui
`modules/excel_export.py`, lengkap dengan:
- Header berwarna coklat dengan teks putih tebal
- Border rapi di seluruh sel
- Lebar kolom otomatis (auto-width) menyesuaikan isi
- Highlight khusus untuk 3 ranking teratas (nuansa sage)
- Sheet kedua "Ringkasan" berisi metode, tanggal export, dan bobot kriteria yang dipakai

## 🎨 Tampilan

UI menggunakan tema **Warm Cafe Aesthetic**:
- Cream `#F8F4EC`, Coklat `#6F4E37`, Sage `#A3B18A`
- Hero banner, dashboard KPI ringkas, kartu konten bergaya cafe
- Grafik Plotly (bar, radar, donut) dengan palet warna senada
- Animasi ringan (fade-in, hover) untuk pengalaman yang lebih modern

## 🛠️ Teknologi

- Python 3.12
- Streamlit (UI)
- Pandas & NumPy (pengolahan data & algoritma)
- Plotly (visualisasi interaktif)
- openpyxl (export Excel profesional)

## 👩‍💻 Metode: TOPSIS

TOPSIS (Technique for Order Preference by Similarity to Ideal Solution) merangking alternatif
berdasarkan jarak terdekat ke **solusi ideal positif** dan jarak terjauh dari **solusi ideal negatif**.

Tahapan: normalisasi matriks → pembobotan → tentukan solusi ideal (+/-) → hitung jarak euclidean
→ hitung skor preferensi (V) → urutkan ranking berdasarkan V tertinggi.
