import streamlit as st
import plotly.express as px

from modules.loader import load_data
from modules.alerts import service_alert, document_alert

master, dokumen, km, qc = load_data()

st.title("🚐 Fleet Management System")

# =====================
# Fleet Overview
# =====================

st.header("Fleet Overview")

col1, col2 = st.columns(2)

col1.metric("Total Kendaraan", len(master))
col2.metric("Data QC", len(qc))

st.dataframe(master)

# =====================
# KM Monitoring
# =====================

st.header("Monitoring KM")

fig = px.bar(
    km,
    x="ID_UNIT",
    y="KM_UPDATE",
    title="KM Kendaraan"
)

st.plotly_chart(fig)

# =====================
# QC Inspection
# =====================

st.header("QC Inspection")

st.dataframe(qc)

# =====================
# Alert Service
# =====================

st.header("⚠ Service Alert")

alert_service = service_alert(km)

st.dataframe(alert_service)

# =====================
# Alert Dokumen
# =====================

st.header("⚠ Dokumen Expired")

alert_doc = document_alert(dokumen)

st.dataframe(alert_doc)