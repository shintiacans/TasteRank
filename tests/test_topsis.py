"""
test_topsis.py
Modul 3 pendukung - unit test & edge case test untuk modul algoritma TOPSIS.
Jalankan dengan: python -m tests.test_topsis  (dari root folder dss_app)
atau: pytest tests/test_topsis.py -v
"""

import sys
import os
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from modules import topsis  # noqa: E402


def test_normal_case():
    """TEST NORMAL: 3 alternatif, 2 kriteria (1 benefit, 1 cost), bobot valid 100%."""
    matriks = pd.DataFrame({
        "Rasa": [8, 6, 9],          # benefit
        "Harga": [20000, 15000, 30000],  # cost
    })
    bobot = {"Rasa": 0.6, "Harga": 0.4}
    jenis = {"Rasa": "benefit", "Harga": "cost"}

    hasil = topsis.hitung_topsis(matriks, bobot, jenis)

    assert len(hasil) == 3
    assert hasil["Ranking"].tolist() == [1, 2, 3]
    assert hasil["Skor_Preferensi"].between(0, 1).all()
    print("[PASS] test_normal_case: ranking & skor preferensi valid (0-1)")


def test_edge_case_bobot_tidak_100_persen():
    """
    EDGE CASE 1: total bobot kriteria TIDAK 100% (mis. 90%).
    Sistem harus menolak dengan error yang jelas, BUKAN crash/silent error.
    """
    matriks = pd.DataFrame({
        "Rasa": [8, 6, 9],
        "Harga": [20000, 15000, 30000],
    })
    bobot_salah = {"Rasa": 0.5, "Harga": 0.4}  # total cuma 90%
    jenis = {"Rasa": "benefit", "Harga": "cost"}

    try:
        topsis.hitung_topsis(matriks, bobot_salah, jenis)
        raise AssertionError("Seharusnya melempar BobotTidakValidError, tapi tidak terjadi!")
    except topsis.BobotTidakValidError as e:
        print(f"[PASS] test_edge_case_bobot_tidak_100_persen: berhasil ditangkap -> {e}")


def test_edge_case_semua_nilai_alternatif_sama():
    """
    EDGE CASE 2: semua alternatif punya nilai identik di semua kriteria.
    Ini membuat D+ = D- = 0 untuk semua baris (kandidat ZeroDivisionError).
    Sistem harus tetap mengembalikan hasil (skor preferensi = 0 untuk semua),
    BUKAN crash atau menghasilkan NaN.
    """
    matriks = pd.DataFrame({
        "Rasa": [7, 7, 7, 7],
        "Harga": [25000, 25000, 25000, 25000],
    })
    bobot = {"Rasa": 0.5, "Harga": 0.5}
    jenis = {"Rasa": "benefit", "Harga": "cost"}

    hasil = topsis.hitung_topsis(matriks, bobot, jenis)

    assert not hasil["Skor_Preferensi"].isnull().any(), "Tidak boleh ada NaN di hasil!"
    assert (hasil["Skor_Preferensi"] == 0.0).all(), "Semua nilai sama -> skor preferensi harus 0 semua"
    print("[PASS] test_edge_case_semua_nilai_alternatif_sama: tidak ada NaN, tidak crash, skor = 0 semua")


def test_edge_case_kolom_bernilai_nol_semua():
    """
    EDGE CASE 3 (bonus): satu kriteria bernilai 0 di semua alternatif
    (mis. semua tempat gratis, harga=0). Penyebut normalisasi jadi 0
    -> harus tetap dihandle tanpa error.
    """
    matriks = pd.DataFrame({
        "Rasa": [8, 6, 9],
        "Harga_Gratis": [0, 0, 0],
    })
    bobot = {"Rasa": 0.7, "Harga_Gratis": 0.3}
    jenis = {"Rasa": "benefit", "Harga_Gratis": "cost"}

    hasil = topsis.hitung_topsis(matriks, bobot, jenis)
    assert not hasil["Skor_Preferensi"].isnull().any()
    print("[PASS] test_edge_case_kolom_bernilai_nol_semua: kolom all-zero tidak menyebabkan NaN")


if __name__ == "__main__":
    test_normal_case()
    test_edge_case_bobot_tidak_100_persen()
    test_edge_case_semua_nilai_alternatif_sama()
    test_edge_case_kolom_bernilai_nol_semua()
    print("\n✅ Semua test PASSED (1 normal case + 3 edge case)")
