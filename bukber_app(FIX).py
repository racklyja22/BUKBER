import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import io

st.set_page_config(
    page_title="Bukber FKMP 2018",
    page_icon="🍽️",
    layout="wide"
)

st.title("🍽️ BUKBER FKMP 2018")
st.write("Silakan pilih menu yang ingin dipesan")

# =========================
# GOOGLE SHEETS SETUP
# =========================
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = "service_account.json"  # file credentials Google Sheets

credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
gc = gspread.authorize(credentials)

SPREADSHEET_NAME = "Bukber_FKMP_2018"
WORKSHEET_NAME = "Rekap_Pesanan"

try:
    sh = gc.open(SPREADSHEET_NAME)
except gspread.SpreadsheetNotFound:
    sh = gc.create(SPREADSHEET_NAME)
try:
    ws = sh.worksheet(WORKSHEET_NAME)
except gspread.WorksheetNotFound:
    ws = sh.add_worksheet(title=WORKSHEET_NAME, rows="1000", cols="10")
    ws.append_row(["Nama", "Menu", "Jumlah", "Harga", "Total"])

# =========================
# DATA MENU
# =========================
menu_kebuli_personal = {
    "Kebuli Ayam Kecil":25000,
    "Kebuli Ayam Besar":35000,
    "Kebuli Ayam Bakar":38000,
    "Kebuli Bebek Goreng":45000,
    "Kebuli Sapi/Iga Bakar":45000,
    "Kebuli Kambing Bakar":45000,
    "Kebuli Rica-rica Kambing":50000
}

menu_nampan_keluarga = {
    "Kebuli Nampan Ayam Goreng":140000,
    "Kebuli Nampan Ayam Bakar":160000,
    "Kebuli Nampan Sapi":180000,
    "Kebuli Nampan Kambing":180000
}

menu_nampan_jumbo = {
    "Kebuli Nampan Jumbo Ayam Goreng":350000,
    "Kebuli Nampan Jumbo Ayam Bakar":380000,
    "Kebuli Nampan Jumbo Sapi":450000,
    "Kebuli Nampan Jumbo Kambing":450000
}

menu_nasi_putih = {
    "Nasi Ayam Goreng Kremes":35000,
    "Nasi Ayam Goreng Cabe Ijo":35000,
    "Nasi Bebek Goreng Kremes":40000,
    "Nasi Bebek Goreng Cabe Ijo":40000,
    "Nasi Ayam Bakar":35000,
    "Nasi Sambal Cumi Pedas":35000,
    "Nasi Putih Iga Bakar":40000,
    "Nasi Putih Kambing Bakar":45000,
    "Nasi Putih Rica Kambing":45000
}

menu_snack = {
    "Bingka Kentang":25000,
    "Samosa (3 pcs)":20000,
    "Puding Karamel":20000,
    "Canai Coklat Keju":20000,
    "Kentang Goreng":18000,
    "Sosis Solo (3 pcs)":18000,
    "Lumpia Mayo Beef (3 pcs)":18000,
    "Buah Potong":15000,
    "Canai Ori":12000
}

menu_kuah = {
    "Gulai Kambing":45000,
    "Sop Iga Sapi":45000,
    "Canai Gulai Kambing":40000
}

menu_tambahan = {
    "Nasi Kebuli":15000,
    "Tempe Goreng":10000,
    "Telur Mata Sapi":7000,
    "Nasi Putih":5000,
    "Emping":5000,
    "Ekstra Kremes":5000,
    "Ekstra Kangkung Goreng":5000,
    "Ekstra Sambal":3000,
    "Ekstra Kerupuk":3000,
    "Ekstra Acar":3000
}

menu_minuman = {
    "Air Es":3000,
    "Air Hangat":3000,
    "Teh Es":7000,
    "Teh Hangat":7000,
    "Kelapa Muda Bijian":20000,
    "Es Tebu Lemon":20000,
    "Milky Strawberry":18000,
    "Milky Chocolate":18000,
    "Cincau Gula Aren":18000,
    "Susu Kurma":15000,
    "Susu Jahe Secang":15000,
    "Teh Tarik":15000,
    "Es Bunga Telang":15000,
    "Es Timun Serut":15000,
    "Jeruk Hangat":12000,
    "Es Jeruk":12000,
    "Lychee Tea":12000,
    "Lemon Tea":12000,
    "Kunyit Asam":12000,
    "Black Coffee":10000,
    "Lemonade":10000,
    "Air Mineral":7000
}

# =========================
# INPUT USER
# =========================
nama = st.text_input("Nama Pemesan")

tabs = st.tabs([
    "🍗 Kebuli",
    "🍛 Nasi",
    "🥘 Kuah",
    "🍟 Snack",
    "➕ Tambahan",
    "🥤 Minuman",
    "🍽️ Nampan"
])

with tabs[0]:
    kebuli = st.selectbox("Menu Kebuli", ["-"] + list(menu_kebuli_personal.keys()))
    qty_kebuli = st.number_input("Jumlah Kebuli", min_value=0, step=1)

with tabs[1]:
    nasi = st.selectbox("Menu Nasi", ["-"] + list(menu_nasi_putih.keys()))
    qty_nasi = st.number_input("Jumlah Nasi", min_value=0, step=1)

with tabs[2]:
    kuah = st.selectbox("Menu Kuah", ["-"] + list(menu_kuah.keys()))
    qty_kuah = st.number_input("Jumlah Kuah", min_value=0, step=1)

with tabs[3]:
    snack = st.selectbox("Menu Snack", ["-"] + list(menu_snack.keys()))
    qty_snack = st.number_input("Jumlah Snack", min_value=0, step=1)

with tabs[4]:
    tambahan = st.selectbox("Menu Tambahan", ["-"] + list(menu_tambahan.keys()))
    qty_tambahan = st.number_input("Jumlah Tambahan", min_value=0, step=1)

with tabs[5]:
    minuman = st.selectbox("Menu Minuman", ["-"] + list(menu_minuman.keys()))
    qty_minuman = st.number_input("Jumlah Minuman", min_value=0, step=1)

with tabs[6]:
    nampan = st.selectbox(
        "Menu Nampan",
        ["-"] + list(menu_nampan_keluarga.keys()) + list(menu_nampan_jumbo.keys())
    )
    qty_nampan = st.number_input("Jumlah Nampan", min_value=0, step=1)

# =========================
# FUNGSI TAMBAH PESANAN KE SHEETS
# =========================
def tambah_ke_sheets(nama, menu, qty, daftar):
    if menu != "-" and qty > 0 and nama.strip():
        harga = daftar[menu]
        total = harga * qty
        ws.append_row([nama, menu, qty, harga, total])

if st.button("➕ Tambah Pesanan"):
    tambah_ke_sheets(nama, kebuli, qty_kebuli, menu_kebuli_personal)
    tambah_ke_sheets(nama, nasi, qty_nasi, menu_nasi_putih)
    tambah_ke_sheets(nama, kuah, qty_kuah, menu_kuah)
    tambah_ke_sheets(nama, snack, qty_snack, menu_snack)
    tambah_ke_sheets(nama, tambahan, qty_tambahan, menu_tambahan)
    tambah_ke_sheets(nama, minuman, qty_minuman, menu_minuman)
    if nampan in menu_nampan_keluarga:
        tambah_ke_sheets(nama, nampan, qty_nampan, menu_nampan_keluarga)
    if nampan in menu_nampan_jumbo:
        tambah_ke_sheets(nama, nampan, qty_nampan, menu_nampan_jumbo)
    st.success(f"Pesanan untuk {nama} ditambahkan!")

# =========================
# LIVE REKAP MULTI-USER
# =========================
st.subheader("🧾 Rekap Pesanan Live")
data = ws.get_all_records()
df_live = pd.DataFrame(data)

if not df_live.empty:
    df_grouped = df_live.groupby("Nama").apply(
        lambda x: pd.Series({
            "Pesanan": " + ".join([f"{row['Menu']} ({row['Jumlah']})" for idx,row in x.iterrows()]),
            "Total": x["Total"].sum()
        })
    ).reset_index()
    for idx,row in df_grouped.iterrows():
        col1,col2 = st.columns([10,1])
        with col1:
            st.markdown(f"**{row['Nama']}** | {row['Pesanan']} = Total Rp {row['Total']:,.0f}")
        with col2:
            if st.button("🗑️ Hapus Pemesan", key=f"hapus_{row['Nama']}"):
                df_live = df_live[df_live["Nama"] != row['Nama']]
                ws.clear()
                ws.append_row(["Nama","Menu","Jumlah","Harga","Total"])
                for i,r in df_live.iterrows():
                    ws.append_row([r['Nama'], r['Menu'], r['Jumlah'], r['Harga'], r['Total']])
else:
    st.info("Belum ada pesanan.")

# =========================
# DOWNLOAD EXCEL SESUAI LIVE REKAP
# =========================
st.subheader("⬇️ Download Rekap Pesanan")
if not df_live.empty:
    buffer = io.BytesIO()
    df_live.to_excel(buffer, index=False, engine="openpyxl")
    buffer.seek(0)
    st.download_button(
        label="⬇️ Download Pesanan (.xlsx)",
        data=buffer,
        file_name="rekap_pesanan.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )