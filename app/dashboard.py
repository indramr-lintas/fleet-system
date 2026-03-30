import streamlit as st
import pandas as pd
import sys
import os

st.set_page_config(
    page_title="Fleet Dashboard",
    layout="wide"
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.loader import load_data
from modules.alerts import service_alert, document_alert
from modules.analytics import km_chart
from modules.styling import highlight_service
from modules.analytics import km_chart, utilization_chart, qc_chart
from modules.fleet_status import fleet_status
from modules.styling import highlight_status
from modules.fleet_board import fleet_control_board
from modules.maintenance_prediction import maintenance_prediction
from modules.tire_monitor import tire_alert
from modules.qc_alert import qc_alert
from modules.qc_board import qc_control_board
from modules.vehicle_detail import vehicle_detail
from modules.crud_master import create_master, update_master, delete_master
from modules.crud_operational import (
    create_qc, update_qc, delete_qc,
    create_km, update_km, delete_km
)
from modules.auth import login

with st.spinner("Loading data..."):
    master, dokumen, km, qc = load_data()

# =====================
# MERGE DATA
# =====================

status_df = master.merge(km, on="ID_UNIT", how="left")

# =====================
# FILTER UNIT
# =====================

# unit_filter = st.selectbox(
#    "Pilih Unit",
#    ["All"] + list(master["ID_UNIT"].unique()),
#    key="filter_unit"
# )

# filter jika dipilih
#if unit_filter != "All":

#    master = master[master["ID_UNIT"] == unit_filter]
#    km = km[km["ID_UNIT"] == unit_filter]
#    qc = qc[qc["ID_UNIT"] == unit_filter]

# =====================
# STATUS ARMADA
# =====================

def get_status(row):

    if row["KM_UPDATE"] > row["KM_SERVICE_NEXT"]:
        return "Service Overdue"

    elif row["KM_SERVICE_NEXT"] - row["KM_UPDATE"] <= 5000:
        return "Service Soon"

    else:
        return "Ready"

status_df["STATUS"] = status_df.apply(get_status, axis=1)

# =====================
# LOGIN SYSTEM
# =====================

if "login_status" not in st.session_state:
    st.session_state.login_status = False

if "role" not in st.session_state:
    st.session_state.role = None


if not st.session_state.login_status:

    st.title("🔐 Login Fleet System")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        status, role = login(username, password)

        if status:
            st.session_state.login_status = True
            st.session_state.role = role
            st.success("Login berhasil")
            st.rerun()
        else:
            st.error("Username / Password salah")

    st.stop()  # ⛔ STOP APP kalau belum login

# =====================
# SIDEBAR
# =====================

st.sidebar.title("Menu")

# 🔐 LOGOUT
if st.sidebar.button("Logout"):
    st.session_state.login_status = False
    st.session_state.role = None
    st.rerun()


# ====================
# Menu
# ====================    

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Dashboard",
        "Fleet Data",
        "Maintenance",
        "QC Inspection",
        "Vehicle Detail",
        "CRUD Master",
        "CRUD QC",
        "CRUD KM"
    ],
    key="menu"
)

menu_options = [
    "Dashboard",
    "Fleet Data",
    "Maintenance"
]

# hanya admin yang bisa akses CRUD
if st.session_state.role == "admin":
    menu_options += ["CRUD Master", "CRUD QC", "CRUD KM"]

menu = st.sidebar.selectbox("Menu", menu_options)


with st.spinner("Loading data..."):
    master, dokumen, km, qc = load_data()

# =====================
# SEARCH UNIT
# =====================

st.sidebar.header("Search")

search_unit = st.sidebar.text_input(
    "Cari ID Unit / Nopol"
)

if search_unit:

    master = master[
        master["ID_UNIT"].astype(str).str.contains(search_unit, case=False) |
        master["NO_POLISI"].astype(str).str.contains(search_unit, case=False)
    ]

    km = km[km["ID_UNIT"].isin(master["ID_UNIT"])]
    qc = qc[qc["ID_UNIT"].isin(master["ID_UNIT"])]
    

# ====================
# Dashboard
# ====================

if menu == "Dashboard":

    st.title("🚐 Fleet Management Dashboard")

    service_due = service_alert(km)
    doc_due = document_alert(dokumen)

    # =====================
    # KPI
    # =====================
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Armada", len(master))
    col2.metric("Service Due", len(service_due))
    col3.metric("Dokumen Expired", len(doc_due))

    st.divider()

    # =====================
    # FLEET STATUS SUMMARY
    # =====================

    ready = status_df[status_df["STATUS"] == "Ready"]
    soon = status_df[status_df["STATUS"] == "Service Soon"]
    overdue = status_df[status_df["STATUS"] == "Service Overdue"]

    st.subheader("🚦 Fleet Readiness Status")

    col1, col2, col3 = st.columns(3)

    col1.metric("🟢 Ready", len(ready))
    col2.metric("🟡 Service Soon", len(soon))
    col3.metric("🔴 Service Overdue", len(overdue))

    st.divider()

    # Grafik
    col1, col2 = st.columns(2)

    with col1:
        fig = km_chart(km)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = qc_chart(qc)
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    fig = utilization_chart(km)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # =====================
    # ALERT SECTION
    # =====================

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("⚠ Service Alert")

        service_due = service_alert(km)

        if service_due.empty:
            st.success("Tidak ada kendaraan yang perlu service")
        else:
            st.dataframe(service_due, use_container_width=True)

    with col2:
        st.subheader("📄 Dokumen Expired")

        doc_due = document_alert(dokumen)

        if doc_due.empty:
            st.success("Tidak ada dokumen yang expired")
        else:
            st.dataframe(doc_due, use_container_width=True)

    

# ====================
# Fleet Data
# ====================

if menu == "Fleet Data":

    fleet_control_board(status_df)

    st.subheader("Fleet Status Board")

    st.dataframe(
        status_df[[
            "ID_UNIT",
            "NO_POLISI",
            "KM_UPDATE",
            "KM_SERVICE_NEXT",
            "STATUS"
        ]].style.apply(highlight_status, axis=1),
        use_container_width=True
    )

    st.title("Data Kendaraan")

    st.dataframe(
        status_df,
        use_container_width=True
    )

# ====================
# Maintenance
# ====================

if menu == "Maintenance":

    st.title("Maintenance Monitoring")

    st.dataframe(
        km.style.apply(highlight_service, axis=1),
        use_container_width=True
    )

    prediction = maintenance_prediction(km)

    st.subheader("🔧 Service Prediction (<5000 KM)")

    st.dataframe(
        prediction,
        use_container_width=True
    )

    st.subheader("🛞 Tire Alert (TWI < 2mm)")

    tire_due = tire_alert(km)

    st.dataframe(
        tire_due,
        use_container_width=True
    )

# ====================
# QC Inspection
# ====================

if menu == "QC Inspection":

    qc_control_board(qc)

    st.divider()

    st.dataframe(qc, use_container_width=True)

    st.subheader("QC Terakhir Kendaraan")

    # pastikan kolom tanggal sudah datetime
    qc["TGL_CEK"] = pd.to_datetime(qc["TGL_CEK"], errors="coerce")

    # ambil data QC terakhir per unit
    qc_latest = qc.sort_values("TGL_CEK").drop_duplicates("ID_UNIT", keep="last")

    st.dataframe(qc_latest.astype(str), width="stretch")

    today = pd.Timestamp.today()

    qc_latest["DAYS"] = (today - qc_latest["TGL_CEK"]).dt.days

    overdue = qc_latest[qc_latest["DAYS"] > 7]

    st.subheader("⚠ QC Belum Dicek > 7 Hari")

    st.dataframe(overdue.astype(str), width="stretch")


# ====================
# Vehicle Detail
# ====================

if menu == "Vehicle Detail":

    st.title("Vehicle Detail")

    unit = st.selectbox(
        "Pilih Unit",
        master["ID_UNIT"].unique()
    )

    vehicle_detail(master, km, dokumen, qc, unit)


# ====================
# CURD Master
# ====================

if menu == "CRUD Master":

    # 🔐 CEK ROLE
    if st.session_state.role != "admin":
        st.warning("Akses ditolak! Hanya admin.")
        st.stop()

    st.title("CRUD Master Kendaraan")

    # LOAD DATA
    master, _, _, _ = load_data()

    # =====================
    # CREATE
    # =====================
    st.subheader("➕ Tambah Data")

    with st.form("form_create"):
        id_unit = st.text_input("ID Unit")
        no_polisi = st.text_input("No Polisi")

        submit = st.form_submit_button("Simpan")

        if submit:

            if not id_unit or not no_polisi:
                st.error("Semua field wajib diisi!")
            
            elif id_unit in master["ID_UNIT"].values:
                st.warning("ID Unit sudah ada!")
            
            else:
                create_master(id_unit, no_polisi)
                st.success("Data berhasil ditambahkan")
                st.cache_data.clear()
                st.rerun()

    st.divider()

    # =====================
    # READ
    # =====================
    st.subheader("📋 Data Master")

    st.dataframe(master, use_container_width=True)

    st.divider()

    # =====================
    # UPDATE & DELETE
    # =====================
    st.subheader("✏️ Edit / Hapus")

    selected_index = st.selectbox(
        "Pilih Data",
        master.index
    )

    row = master.loc[selected_index]

    new_id = st.text_input("ID Unit (Edit)", row["ID_UNIT"])
    new_nopol = st.text_input("No Polisi (Edit)", row["NO_POLISI"])

    col1, col2 = st.columns(2)

    with col1:
        id_unit = st.selectbox("ID Unit", master["ID_UNIT"])

    with col2:
        no_polisi = st.text_input("No Polisi")

# ====================
# CURD QC
# ====================

if menu == "CRUD QC":

    st.title("QC Inspection")

    _, _, _, qc = load_data()

    # CREATE
    st.subheader("➕ Input QC")

    with st.form("form_qc"):

        master, _, _, _ = load_data()

        id_unit = st.selectbox(
            "Pilih ID Unit",
            master["ID_UNIT"].unique()
        )
        from datetime import datetime

        tgl = datetime.now()
        kondisi = st.text_input("Kondisi")

        submit = st.form_submit_button("Simpan")

        if submit:

            if not id_unit or not kondisi:
                st.error("Data belum lengkap!")
            
            else:
                create_qc([id_unit, str(tgl), kondisi])
                st.success("QC berhasil ditambahkan")
                st.cache_data.clear()
                st.rerun()

    st.divider()

    # READ
    st.dataframe(qc, use_container_width=True)

    st.divider()

    # UPDATE & DELETE
    idx = st.selectbox("Pilih Data", qc.index)

    row = qc.loc[idx]

    new_kondisi = st.text_input("Edit Kondisi", row.iloc[2])

    col1, col2 = st.columns(2)

    with col1:
        id_unit = st.selectbox("ID Unit", master["ID_UNIT"])

    with col2:
        no_polisi = st.text_input("No Polisi")

# ====================
# CURD KM
# ====================

if menu == "CRUD KM":

    st.title("Monitoring KM")

    _, _, km, _ = load_data()

    # CREATE
    st.subheader("➕ Input KM")

    with st.form("form_km"):

        id_unit = st.selectbox(
            "Pilih ID Unit",
            master["ID_UNIT"].unique()
        )
        km_update = st.number_input("KM Update")
        km_next = st.number_input("KM Service Next")

        submit = st.form_submit_button("Simpan")

        if submit:

            if km_update <= 0:
                st.error("KM tidak valid!")
            
            elif km_next <= km_update:
                st.warning("KM service harus lebih besar dari KM update!")
            
            else:
                create_km([id_unit, km_update, km_next])
                st.success("Data KM berhasil ditambahkan")
                st.cache_data.clear()
                st.rerun()

    st.divider()

    # READ
    st.dataframe(km, use_container_width=True)

    st.divider()

    # UPDATE & DELETE
    idx = st.selectbox("Pilih Data KM", km.index)

    row = km.loc[idx]

    new_km = st.number_input("Edit KM", value=int(row.iloc[1]))

    col1, col2 = st.columns(2)

    with col1:
        id_unit = st.selectbox("ID Unit", master["ID_UNIT"])

    with col2:
        no_polisi = st.text_input("No Polisi")
        

if st.session_state.role == "admin":
    if st.button("Delete"):
        delete_master(row_index)
        st.cache_data.clear()
        st.rerun()
else:
    st.info("Hanya admin yang bisa hapus data")

 