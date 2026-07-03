"""
data_handler.py
Modul 1/3 (Data Layer) - bertugas membaca, memvalidasi, dan menyiapkan
data mentah (alternatif x kriteria) sebelum masuk ke modul algoritma TOPSIS.
"""

import pandas as pd

# Definisi 7 kriteria wajib beserta jenisnya (benefit/cost)
# Format: nama_kolom -> ("Label tampilan", "benefit"/"cost", bobot_default)
KRITERIA_CONFIG = {
    "Harga_Rata2_Porsi":   {"label": "💰 Harga Rata-rata/Porsi (Rp)", "jenis": "cost",    "bobot_default": 0.20},
    "Rasa":                {"label": "😋 Rasa (1-10)",                "jenis": "benefit", "bobot_default": 0.20},
    "Jarak_km":            {"label": "📍 Jarak (km)",                 "jenis": "cost",    "bobot_default": 0.15},
    "Kebersihan":          {"label": "✨ Kebersihan (1-10)",          "jenis": "benefit", "bobot_default": 0.15},
    "Rating_Online":       {"label": "⭐ Rating Online (1-5)",        "jenis": "benefit", "bobot_default": 0.15},
    "Waktu_Tunggu_menit":  {"label": "⏱️ Waktu Tunggu (menit)",       "jenis": "cost",    "bobot_default": 0.10},
    "Variasi_Menu":        {"label": "🍽️ Variasi Menu (1-10)",       "jenis": "benefit", "bobot_default": 0.05},
}

KOLOM_ID = "ID"
KOLOM_NAMA = "Nama_Tempat_Makan"


def load_dataset(filepath_or_buffer) -> pd.DataFrame:
    """Membaca dataset CSV tempat makan dan memvalidasi struktur kolomnya."""
    df = pd.read_csv(filepath_or_buffer)
    validate_dataset(df)
    return df


def validate_dataset(df: pd.DataFrame) -> None:
    """
    Validasi struktur dataset.
    Raises ValueError jika kolom wajib tidak lengkap atau tipe data salah.
    """
    kolom_wajib = [KOLOM_ID, KOLOM_NAMA] + list(KRITERIA_CONFIG.keys())
    kolom_hilang = [k for k in kolom_wajib if k not in df.columns]
    if kolom_hilang:
        raise ValueError(f"Dataset tidak lengkap. Kolom hilang: {kolom_hilang}")

    if len(df) < 2:
        raise ValueError("Dataset harus punya minimal 2 alternatif untuk bisa dirangking.")

    for kolom in KRITERIA_CONFIG.keys():
        if not pd.api.types.is_numeric_dtype(df[kolom]):
            raise ValueError(f"Kolom kriteria '{kolom}' harus berisi angka, ditemukan data non-numerik.")
        if df[kolom].isnull().any():
            raise ValueError(f"Kolom kriteria '{kolom}' memiliki nilai kosong (NaN).")


def get_matriks_keputusan(df: pd.DataFrame) -> pd.DataFrame:
    """Mengambil hanya kolom kriteria (matriks keputusan) dari dataframe penuh."""
    return df[list(KRITERIA_CONFIG.keys())].copy()


def get_jenis_kriteria() -> dict:
    """Mengembalikan dict {nama_kolom: 'benefit'/'cost'}."""
    return {k: v["jenis"] for k, v in KRITERIA_CONFIG.items()}


def get_bobot_default() -> dict:
    """Mengembalikan dict {nama_kolom: bobot_default} (total = 1.0 / 100%)."""
    return {k: v["bobot_default"] for k, v in KRITERIA_CONFIG.items()}


def get_label_kriteria() -> dict:
    return {k: v["label"] for k, v in KRITERIA_CONFIG.items()}
