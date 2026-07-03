"""
topsis.py
Modul 2/3 (Logic Layer) - implementasi murni algoritma TOPSIS
(Technique for Order Preference by Similarity to Ideal Solution).

Tidak ada kode UI di sini sama sekali -> supaya bisa dites secara
independen (lihat tests/test_topsis.py) dan dipakai ulang di modul lain.
"""

import numpy as np
import pandas as pd


class BobotTidakValidError(Exception):
    """Dilempar saat total bobot kriteria tidak sama dengan 100% (1.0)."""
    pass


def validasi_bobot(bobot: dict, toleransi: float = 0.001) -> None:
    """
    Memastikan total bobot = 1.0 (100%).
    toleransi dipakai untuk mengatasi floating point error kecil.
    """
    total = sum(bobot.values())
    if abs(total - 1.0) > toleransi:
        raise BobotTidakValidError(
            f"Total bobot harus 100%, saat ini {total*100:.2f}%. "
            f"Selisih {abs(total-1.0)*100:.2f} poin persen."
        )


def normalisasi_matriks(matriks: pd.DataFrame) -> pd.DataFrame:
    """
    Langkah 1 TOPSIS: normalisasi vektor.
    r_ij = x_ij / sqrt(sum(x_ij^2)) untuk setiap kolom j.

    Edge case: jika sebuah kolom memiliki semua nilai 0 (pembagi = 0),
    hasil dinormalisasi jadi 0 untuk menghindari ZeroDivisionError/NaN.
    """
    matriks = matriks.astype(float)
    penyebut = np.sqrt((matriks ** 2).sum(axis=0))
    penyebut_aman = penyebut.replace(0, np.nan)  # hindari div by zero
    hasil = matriks.div(penyebut_aman, axis=1)
    hasil = hasil.fillna(0.0)  # kolom yang penyebutnya 0 -> normalisasi 0
    return hasil


def matriks_terbobot(matriks_normal: pd.DataFrame, bobot: dict) -> pd.DataFrame:
    """Langkah 2 TOPSIS: y_ij = r_ij * w_j."""
    return matriks_normal.mul(pd.Series(bobot), axis=1)


def solusi_ideal(matriks_terbobot: pd.DataFrame, jenis_kriteria: dict) -> tuple[pd.Series, pd.Series]:
    """
    Langkah 3 TOPSIS: tentukan solusi ideal positif (A+) dan negatif (A-).
    - Kriteria benefit -> A+ = max, A- = min
    - Kriteria cost    -> A+ = min, A- = max
    """
    a_plus, a_minus = {}, {}
    for kolom in matriks_terbobot.columns:
        if jenis_kriteria[kolom] == "benefit":
            a_plus[kolom] = matriks_terbobot[kolom].max()
            a_minus[kolom] = matriks_terbobot[kolom].min()
        else:  # cost
            a_plus[kolom] = matriks_terbobot[kolom].min()
            a_minus[kolom] = matriks_terbobot[kolom].max()
    return pd.Series(a_plus), pd.Series(a_minus)


def jarak_ke_solusi_ideal(matriks_terbobot: pd.DataFrame, a_plus: pd.Series, a_minus: pd.Series):
    """Langkah 4 TOPSIS: hitung jarak euclidean tiap alternatif ke A+ dan A-."""
    d_plus = np.sqrt(((matriks_terbobot - a_plus) ** 2).sum(axis=1))
    d_minus = np.sqrt(((matriks_terbobot - a_minus) ** 2).sum(axis=1))
    return d_plus, d_minus


def nilai_preferensi(d_plus: pd.Series, d_minus: pd.Series) -> pd.Series:
    """
    Langkah 5 TOPSIS: V_i = D-_i / (D+_i + D-_i)
    Semakin besar V_i, semakin dekat ke solusi ideal -> semakin baik.

    Edge case: jika D+ dan D- keduanya 0 (alternatif identik dengan
    solusi ideal & anti-ideal sekaligus -- hanya mungkin saat SEMUA
    alternatif punya nilai sama persis di semua kriteria), preferensi
    diset 0 untuk semua agar tidak terjadi ZeroDivisionError/NaN.
    """
    penyebut = d_plus + d_minus
    penyebut_aman = penyebut.replace(0, np.nan)
    v = d_minus / penyebut_aman
    v = v.fillna(0.0)
    return v


def hitung_topsis(matriks: pd.DataFrame, bobot: dict, jenis_kriteria: dict) -> pd.DataFrame:
    """
    Fungsi utama: menjalankan seluruh pipeline TOPSIS dan mengembalikan
    dataframe hasil (skor preferensi + ranking), diurutkan dari terbaik.

    Raises:
        BobotTidakValidError: jika total bobot != 100%
    """
    validasi_bobot(bobot)

    r = normalisasi_matriks(matriks)
    y = matriks_terbobot(r, bobot)
    a_plus, a_minus = solusi_ideal(y, jenis_kriteria)
    d_plus, d_minus = jarak_ke_solusi_ideal(y, a_plus, a_minus)
    v = nilai_preferensi(d_plus, d_minus)

    hasil = pd.DataFrame({
        "D_Plus": d_plus,
        "D_Minus": d_minus,
        "Skor_Preferensi": v,
    })
    hasil = hasil.sort_values("Skor_Preferensi", ascending=False)
    hasil["Ranking"] = range(1, len(hasil) + 1)
    return hasil
