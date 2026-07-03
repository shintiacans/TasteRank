"""
app.py
Modul 3/3 (Presentation/UI Layer) - antarmuka Streamlit untuk aplikasi
DSS Pemilihan Tempat Makan menggunakan metode TOPSIS.

Modul ini HANYA mengurus tampilan & interaksi. Logika data ada di
modules/data_handler.py, logika algoritma ada di modules/topsis.py,
dan logika export Excel ada di modules/excel_export.py.

Tema tampilan: Warm Cafe Aesthetic (cream, coklat, sage).
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from modules import data_handler
from modules import topsis
from modules import excel_export

# ----------------------------------------------------------------------------
# KONFIGURASI HALAMAN
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="YumRank ☕ DSS Tempat Makan",
    page_icon="☕",
    layout="wide",
)

# ----------------------------------------------------------------------------
# STYLING - WARM CAFE AESTHETIC THEME
# ----------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@500;600;700;800&family=Nunito+Sans:wght@400;500;600;700&display=swap');

:root{
    --cream: #F8F4EC;
    --cream-soft: #FBF8F2;
    --coklat: #6F4E37;
    --coklat-dark: #4A3423;
    --coklat-light: #9C7B5F;
    --sage: #A3B18A;
    --sage-light: #E3E9D8;
    --sage-dark: #7C8C63;
    --text-main: #4A3423;
}

html, body, [class*="css"]  {
    font-family: 'Nunito Sans', sans-serif;
    color: var(--text-main);
}

.stApp {
    background: linear-gradient(180deg, var(--cream) 0%, #F1EADC 100%);
}

h1, h2, h3, h4 {
    font-family: 'Fraunces', serif !important;
    color: var(--coklat) !important;
    font-weight: 700 !important;
}

/* Subtle fade-in animation for main blocks */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.block-container { animation: fadeInUp 0.5s ease-out; }

/* Hero banner */
.hero-banner {
    background: linear-gradient(120deg, var(--coklat) 0%, #8A6448 55%, var(--sage-dark) 130%);
    border-radius: 24px;
    padding: 36px 40px;
    margin-bottom: 24px;
    box-shadow: 0 12px 28px rgba(74, 52, 35, 0.25);
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: "☕ 🍜 🍰 🥗 🍕";
    position: absolute;
    right: -10px;
    top: -18px;
    font-size: 3.4rem;
    opacity: 0.16;
    letter-spacing: 14px;
    transform: rotate(8deg);
}
.hero-banner h1 {
    color: #FFFFFF !important;
    font-size: 2.5rem;
    margin: 0;
    font-family: 'Fraunces', serif !important;
}
.hero-banner p {
    color: #F3E9DC;
    font-size: 1.05rem;
    margin-top: 8px;
    max-width: 640px;
}
.hero-badges { margin-top: 16px; }

/* Sticker / badge pill */
.badge {
    display: inline-block;
    background: rgba(255,255,255,0.16);
    border: 1px solid rgba(255,255,255,0.35);
    border-radius: 999px;
    padding: 5px 14px;
    font-weight: 600;
    font-size: 0.82rem;
    color: #FFFFFF;
    margin-right: 8px;
}

/* Dashboard KPI cards */
.kpi-card {
    background: #FFFFFF;
    border: 1px solid var(--sage-light);
    border-left: 5px solid var(--sage);
    border-radius: 16px;
    padding: 16px 20px;
    box-shadow: 0 4px 14px rgba(111, 78, 55, 0.06);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(111, 78, 55, 0.14);
}
.kpi-label {
    font-size: 0.8rem;
    color: var(--coklat-light);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin: 0;
}
.kpi-value {
    font-size: 1.7rem;
    color: var(--coklat) !important;
    font-family: 'Fraunces', serif;
    font-weight: 700;
    margin: 2px 0 0 0;
}

/* Content card */
.cafe-card {
    background: #FFFFFF;
    border: 1px solid #EDE6D8;
    border-radius: 20px;
    padding: 20px 24px;
    margin-bottom: 18px;
    box-shadow: 0 4px 16px rgba(111, 78, 55, 0.06);
}

/* Podium rank 1/2/3 */
.podium-card {
    border-radius: 18px;
    padding: 20px 16px;
    text-align: center;
    box-shadow: 0 6px 18px rgba(111, 78, 55, 0.14);
    transition: transform 0.25s ease;
}
.podium-card:hover { transform: translateY(-4px) scale(1.01); }
.podium-1 { background: linear-gradient(160deg, #E7CB8E, #C89B4A); }
.podium-2 { background: linear-gradient(160deg, #DCE3D0, #B9C6A6); }
.podium-3 { background: linear-gradient(160deg, #E3CBB4, #C79E7B); }
.podium-card h2 { color: var(--coklat-dark) !important; margin: 6px 0 2px 0; font-size: 1.25rem; }
.podium-card .medal { font-size: 2.4rem; }
.podium-card .skor-text { color: var(--coklat-dark); font-weight: 700; }

/* Buttons */
.stButton>button, .stDownloadButton>button {
    background: var(--coklat);
    color: #FFFFFF;
    border-radius: 999px;
    border: none;
    padding: 10px 26px;
    font-weight: 600;
    box-shadow: 0 4px 10px rgba(111, 78, 55, 0.3);
    transition: all 0.2s ease;
}
.stButton>button:hover, .stDownloadButton>button:hover {
    background: var(--sage-dark);
    transform: translateY(-1px);
    box-shadow: 0 6px 14px rgba(124, 140, 99, 0.35);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #F1E9D8, var(--cream-soft));
    border-right: 1px solid #E4D9C4;
}
section[data-testid="stSidebar"] h3 { color: var(--coklat) !important; }

/* Slider accent */
.stSlider [data-baseweb="slider"] > div > div { background: var(--sage) !important; }

/* Metric */
[data-testid="stMetric"] {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 10px 14px;
    border: 1px solid var(--sage-light);
}

/* Dataframe corners */
[data-testid="stDataFrame"] { border-radius: 16px; overflow: hidden; }

/* Divider dots */
.cafe-divider {
    text-align: center;
    color: var(--sage-dark);
    letter-spacing: 8px;
    margin: 6px 0 18px 0;
    opacity: 0.7;
}

footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# Skala warna warm cafe untuk chart Plotly (cream -> sage -> coklat)
CAFE_SCALE = ["#F8F4EC", "#D9C9A3", "#A3B18A", "#7C8C63", "#6F4E37"]
COKLAT = "#6F4E37"
SAGE = "#A3B18A"
SAGE_DARK = "#7C8C63"
CREAM = "#F8F4EC"

# ----------------------------------------------------------------------------
# HEADER / HERO BANNER
# ----------------------------------------------------------------------------
st.markdown("""
<div class="hero-banner">
    <h1>☕ YumRank — DSS Pemilihan Tempat Makan</h1>
    <p>Bingung mau makan di mana? Temukan tempat makan terbaik versimu dengan metode
    ilmiah TOPSIS — geser bobot kriteria dan lihat ranking berubah secara real-time.</p>
    <div class="hero-badges">
        <span class="badge">📊 Metode TOPSIS</span>
        <span class="badge">🎚️ What-If Analysis</span>
        <span class="badge">📥 Export Excel</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# SIDEBAR - UPLOAD DATA & BOBOT (WHAT-IF)
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🍽️ Data & Pengaturan")

    sumber = st.radio("Sumber dataset", ["📁 Gunakan dataset contoh", "⬆️ Upload CSV sendiri"])

    if sumber == "⬆️ Upload CSV sendiri":
        file_upload = st.file_uploader("Upload file CSV", type=["csv"])
    else:
        file_upload = "data/tempat_makan.csv"

    st.markdown("---")
    st.markdown("### 🎚️ What-If: Atur Bobot Kriteria")
    st.caption("Geser slider untuk mengubah prioritas — ranking akan otomatis update! 🔄")

    label_kriteria = data_handler.get_label_kriteria()
    bobot_default = data_handler.get_bobot_default()

    bobot_input = {}
    for kolom, label in label_kriteria.items():
        default_persen = int(round(bobot_default[kolom] * 100))
        bobot_input[kolom] = st.slider(label, 0, 100, default_persen, 1, key=f"slider_{kolom}")

    total_bobot = sum(bobot_input.values())
    warna_total = "🟢" if total_bobot == 100 else "🔴"
    st.markdown(f"**{warna_total} Total bobot: {total_bobot}%**")
    if total_bobot != 100:
        st.warning(f"⚠️ Total bobot harus tepat 100%! Selisih: {100 - total_bobot:+d}%")

# ----------------------------------------------------------------------------
# LOAD DATA
# ----------------------------------------------------------------------------
if file_upload is None:
    st.info("👈 Silakan upload dataset CSV kamu dulu di sidebar, ya!")
    st.stop()

try:
    df = data_handler.load_dataset(file_upload)
except ValueError as e:
    st.error(f"❌ Dataset bermasalah: {e}")
    st.stop()

# ---- Dashboard KPI ringkas ----
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi_items = [
    (kpi1, "🏠 Total Alternatif", f"{len(df)}"),
    (kpi2, "📋 Jumlah Kriteria", f"{len(label_kriteria)}"),
    (kpi3, "💰 Harga Termurah", f"Rp{int(df['Harga_Rata2_Porsi'].min()):,}".replace(",", ".")),
    (kpi4, "⭐ Rating Tertinggi", f"{df['Rating_Online'].max():.1f} / 5"),
]
for col, label, value in kpi_items:
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <p class="kpi-label">{label}</p>
            <p class="kpi-value">{value}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown('<div class="cafe-card">', unsafe_allow_html=True)
st.markdown(f"#### 📋 Dataset: {len(df)} Alternatif Tempat Makan × {len(label_kriteria)} Kriteria")
st.dataframe(df, use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# HITUNG TOPSIS
# ----------------------------------------------------------------------------
st.markdown("## 🏆 Hasil Ranking")
st.markdown('<div class="cafe-divider">• • •</div>', unsafe_allow_html=True)

if total_bobot != 100:
    st.error("🙅 Ranking belum bisa dihitung karena total bobot belum 100%. Yuk perbaiki slider di sidebar dulu!")
    st.stop()

bobot_normal = {k: v / 100 for k, v in bobot_input.items()}
matriks = data_handler.get_matriks_keputusan(df)
jenis_kriteria = data_handler.get_jenis_kriteria()

try:
    hasil = topsis.hitung_topsis(matriks, bobot_normal, jenis_kriteria)
except topsis.BobotTidakValidError as e:
    st.error(f"❌ {e}")
    st.stop()

hasil_gabung = df.join(hasil)
hasil_gabung = hasil_gabung.sort_values("Ranking")

# ---- Podium top 3 ----
top3 = hasil_gabung.head(3).reset_index(drop=True)
if len(top3) >= 3:
    col2, col1, col3 = st.columns(3)
    medali = ["🥈", "🥇", "🥉"]
    kelas = ["podium-2", "podium-1", "podium-3"]
    kolom_urut = [col2, col1, col3]
    urutan_data = [top3.iloc[1], top3.iloc[0], top3.iloc[2]]
    for col, kelas_css, medal, row in zip(kolom_urut, kelas, medali, urutan_data):
        with col:
            st.markdown(f"""
            <div class="podium-card {kelas_css}">
                <div class="medal">{medal}</div>
                <h2>{row[data_handler.KOLOM_NAMA]}</h2>
                <span class="skor-text">Skor: {row['Skor_Preferensi']:.4f}</span>
            </div>
            """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---- Tabel ranking lengkap ----
st.markdown('<div class="cafe-card">', unsafe_allow_html=True)
st.markdown("#### 📊 Tabel Ranking Lengkap")
tampil = hasil_gabung[[
    "Ranking", data_handler.KOLOM_NAMA, "Skor_Preferensi", "D_Plus", "D_Minus"
]].rename(columns={
    data_handler.KOLOM_NAMA: "Nama Tempat Makan",
    "Skor_Preferensi": "Skor Preferensi",
    "D_Plus": "Jarak ke Ideal (+)",
    "D_Minus": "Jarak ke Anti-Ideal (-)",
})
st.dataframe(
    tampil.style.format({
        "Skor Preferensi": "{:.4f}",
        "Jarak ke Ideal (+)": "{:.4f}",
        "Jarak ke Anti-Ideal (-)": "{:.4f}",
    }).background_gradient(subset=["Skor Preferensi"], cmap="Greens"),
    use_container_width=True, hide_index=True, height=420,
)
st.markdown('</div>', unsafe_allow_html=True)

# ---- Visualisasi ----
st.markdown('<div class="cafe-card">', unsafe_allow_html=True)
st.markdown("#### 📈 Visualisasi Skor Preferensi (Semua Alternatif)")
fig = px.bar(
    hasil_gabung,
    x="Skor_Preferensi",
    y=data_handler.KOLOM_NAMA,
    orientation="h",
    color="Skor_Preferensi",
    color_continuous_scale=CAFE_SCALE,
    text="Skor_Preferensi",
)
fig.update_traces(
    texttemplate="%{text:.3f}",
    textposition="outside",
    marker_line_color=COKLAT,
    marker_line_width=0.6,
)
fig.update_layout(
    yaxis={"categoryorder": "total ascending"},
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    height=780,
    font=dict(family="Nunito Sans, sans-serif", color=COKLAT),
    title_font=dict(family="Fraunces, serif", color=COKLAT, size=18),
    xaxis_title="Skor Preferensi TOPSIS",
    yaxis_title="",
    showlegend=False,
    margin=dict(l=10, r=40, t=20, b=10),
)
fig.update_xaxes(gridcolor="#EDE6D8")
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---- Radar chart top 5 (bonus) ----
st.markdown('<div class="cafe-card">', unsafe_allow_html=True)
st.markdown("#### 🕸️ Profil Kriteria — Top 5 Tempat Makan")
top5 = hasil_gabung.head(5)
kolom_kriteria = list(label_kriteria.keys())

radar_colors = [COKLAT, SAGE_DARK, "#C89B4A", SAGE, "#9C7B5F"]
fig2 = go.Figure()
for i, (_, row) in enumerate(top5.iterrows()):
    nilai = matriks.loc[row.name, kolom_kriteria]
    nilai_norm = (nilai - matriks[kolom_kriteria].min()) / (matriks[kolom_kriteria].max() - matriks[kolom_kriteria].min() + 1e-9)
    warna = radar_colors[i % len(radar_colors)]
    fig2.add_trace(go.Scatterpolar(
        r=nilai_norm.tolist() + [nilai_norm.tolist()[0]],
        theta=[label_kriteria[k] for k in kolom_kriteria] + [label_kriteria[kolom_kriteria[0]]],
        fill='toself',
        name=row[data_handler.KOLOM_NAMA],
        line=dict(color=warna, width=2),
        opacity=0.75,
    ))
fig2.update_layout(
    polar=dict(
        bgcolor="rgba(0,0,0,0)",
        radialaxis=dict(visible=True, range=[0, 1], gridcolor="#EDE6D8"),
        angularaxis=dict(gridcolor="#EDE6D8"),
    ),
    height=520,
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Nunito Sans, sans-serif", color=COKLAT),
    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
    margin=dict(l=30, r=30, t=20, b=10),
)
st.plotly_chart(fig2, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---- Distribusi bobot kriteria (donut) ----
st.markdown('<div class="cafe-card">', unsafe_allow_html=True)
st.markdown("#### 🍩 Distribusi Bobot Kriteria Saat Ini")
fig3 = go.Figure(data=[go.Pie(
    labels=[label_kriteria[k] for k in kolom_kriteria],
    values=[bobot_input[k] for k in kolom_kriteria],
    hole=0.55,
    marker=dict(colors=CAFE_SCALE * 2, line=dict(color="#FFFFFF", width=2)),
    textinfo="label+percent",
    textfont=dict(family="Nunito Sans, sans-serif", size=11, color=COKLAT),
)])
fig3.update_layout(
    height=440,
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Nunito Sans, sans-serif", color=COKLAT),
    showlegend=False,
    margin=dict(l=10, r=10, t=10, b=10),
)
st.plotly_chart(fig3, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---- Download hasil (Excel) ----
st.markdown('<div class="cafe-card">', unsafe_allow_html=True)
st.markdown("#### 📥 Export Hasil Ranking")
st.caption("Unduh hasil ranking lengkap dalam format Excel (.xlsx) dengan tampilan rapi dan profesional.")

bobot_info_export = {label_kriteria[k]: bobot_input[k] for k in kolom_kriteria}
excel_bytes = excel_export.buat_excel_hasil_ranking(
    df_tampil=tampil,
    nama_aplikasi="YumRank — DSS Pemilihan Tempat Makan",
    metode="TOPSIS",
    bobot_info=bobot_info_export,
)

st.download_button(
    "📥 Download Hasil Ranking (Excel .xlsx)",
    data=excel_bytes,
    file_name="hasil_ranking_topsis.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; margin-top:30px; color:#9C7B5F;">
    ☕ Dibuat dengan Streamlit & TOPSIS — Selamat memilih tempat makan favoritmu! 🍰🍜
</div>
""", unsafe_allow_html=True)
