import streamlit as st
import pandas as pd
import os
import io
from streamlit_autorefresh import st_autorefresh  # auto-refresh fix

st.set_page_config(
    page_title="Bukber FKMP 2018",
    page_icon="🍽️",
    layout="wide"
)

# =========================
# AUTO REFRESH (10 detik)
# =========================
st_autorefresh(interval=10000, key="live_rekap_refresh")

st.title("🍽️ BUKBER FKMP 2018")
st.write("Silakan pilih menu yang ingin dipesan")

FILE = "rekap_pesanan.xlsx"

# =========================
# SESSION CART
# =========================
if "cart" not in st.session_state:
    st.session_state.cart = {}  # keyed by Nama

# =========================
# LOAD PESANAN LAMA DARI EXCEL KE SESSION_STATE CART
# =========================
if os.path.exists(FILE) and not st.session_state.cart:
    df_existing = pd.read_excel(FILE, engine='openpyxl')
    for idx, row in df_existing.iterrows():
        nama_existing = row["Nama"]
        if nama_existing not in st.session_state.cart:
            st.session_state.cart[nama_existing] = []
        st.session_state.cart[nama_existing].append({
            "Menu": row["Menu"],
            "Jumlah": row["Jumlah"],
            "Harga": row["Harga"],
            "Total": row["Total"]
        })

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
    "Teh Hangat":7000,
    "Es Teh":7000,
    "Air Hangat":3000,
    "Air Es":3000,
    "Teh Es":7000,
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
# FUNGSI TAMBAH PESANAN
# =========================
def tambah(menu, qty, daftar):
    if menu != "-" and qty > 0 and nama.strip():
        harga = daftar[menu]
        total = harga * qty
        if nama in st.session_state.cart:
            updated = False
            for item in st.session_state.cart[nama]:
                if item["Menu"] == menu:
                    item["Jumlah"] += qty
                    item["Total"] = item["Jumlah"] * item["Harga"]
                    updated = True
                    break
            if not updated:
                st.session_state.cart[nama].append({
                    "Menu": menu,
                    "Jumlah": qty,
                    "Harga": harga,
                    "Total": total
                })
        else:
            st.session_state.cart[nama] = [{
                "Menu": menu,
                "Jumlah": qty,
                "Harga": harga,
                "Total": total
            }]

# =========================
# TOMBOL TAMBAH PESANAN
# =========================
if st.button("➕ Tambah Pesanan"):
    if not nama.strip():
        st.warning("Masukkan Nama Pemesan sebelum menambahkan pesanan!")
    else:
        tambah(kebuli, qty_kebuli, menu_kebuli_personal)
        tambah(nasi, qty_nasi, menu_nasi_putih)
        tambah(kuah, qty_kuah, menu_kuah)
        tambah(snack, qty_snack, menu_snack)
        tambah(tambahan, qty_tambahan, menu_tambahan)
        tambah(minuman, qty_minuman, menu_minuman)
        if nampan in menu_nampan_keluarga:
            tambah(nampan, qty_nampan, menu_nampan_keluarga)
        if nampan in menu_nampan_jumbo:
            tambah(nampan, qty_nampan, menu_nampan_jumbo)
        st.success(f"Pesanan untuk {nama} ditambahkan ke keranjang!")

# =========================
# FUNGSI LOAD FILE
# =========================
def get_rekap_df():
    return pd.DataFrame(columns=["Nama","Menu","Jumlah","Harga","Total"])

# =========================
# GABUNG DATA CART + FILE
# =========================
rows_cart=[]
for n,items in st.session_state.cart.items():
    for i in items:
        rows_cart.append({"Nama":n,"Menu":i["Menu"],"Jumlah":i["Jumlah"],"Harga":i["Harga"],"Total":i["Total"]})

df_live = pd.DataFrame(rows_cart)
st.session_state.df_live = df_live

# =========================
# LIVE REKAP 1 TABEL PER PEMESAN
# =========================
st.subheader("🧾 Rekap Pesanan Live")
df_live = st.session_state.df_live
if not df_live.empty:
    df_grouped = df_live.groupby("Nama").apply(
        lambda x: pd.Series({
            "Pesanan": " + ".join([f"{row['Menu']} ({row['Jumlah']})" for idx,row in x.iterrows()]),
            "Total": x["Total"].sum()
        })
    ).reset_index()

    hapus_list = []
    for idx,row in df_grouped.iterrows():
        col1, col2 = st.columns([10,1])
        with col1:
            st.markdown(f"**{row['Nama']}** | {row['Pesanan']} = Total Rp {row['Total']:,.0f}")
        with col2:
            if st.button("🗑️ Hapus Pemesan", key=f"hapus_{row['Nama']}"):
                hapus_list.append(row['Nama'])

    for nama_hapus in hapus_list:
        df_live = df_live[df_live["Nama"] != nama_hapus]
        if nama_hapus in st.session_state.cart:
            del st.session_state.cart[nama_hapus]
        st.session_state.df_live = df_live

else:
    st.info("Belum ada pesanan.")

# =========================
# TOMBOL DOWNLOAD EXCEL
# =========================
st.subheader("⬇️ Download Rekap Pesanan")
if not df_live.empty:
    buffer = io.BytesIO()
    df_live.to_excel(buffer,index=False,engine="openpyxl")
    buffer.seek(0)
    st.download_button(
        label="⬇️ Download Pesanan (.xlsx)",
        data=buffer,
        file_name="rekap_pesanan.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("Belum ada pesanan untuk di-download.")
