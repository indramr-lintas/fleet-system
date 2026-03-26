import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

@st.cache_data(ttl=300) # 5 menit
def load_data():

def load_data():

creds_dict = st.secrets["gcp_service_account"]

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    creds_dict,
    scopes=scope
)

client = gspread.authorize(creds)

sheet = client.open_by_url(
    "https://docs.google.com/spreadsheets/d/1NiEwbJBUG_0vGBlCgEVNM-Q-uTzn8q0pS3q5MhB-So4"
)

master = pd.DataFrame(sheet.worksheet("MASTER_KENDARAAN").get_all_records())
dokumen = pd.DataFrame(sheet.worksheet("DOKUMEN_KENDARAAN").get_all_records())
km = pd.DataFrame(sheet.worksheet("MONITORING_KM").get_all_records())
qc = pd.DataFrame(sheet.worksheet("QC_INSPECTION").get_all_records())

# Bersihkan data KM
km["KM_UPDATE"] = pd.to_numeric(
    km["KM_UPDATE"].astype(str).str.replace(",", ""),
    errors="coerce"
)

km["KM_SERVICE_NEXT"] = pd.to_numeric(
    km["KM_SERVICE_NEXT"].astype(str).str.replace(",", ""),
    errors="coerce"
)

return master, dokumen, km, qc