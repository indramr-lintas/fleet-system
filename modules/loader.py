import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials


def load_data():

    creds_dict = st.secrets["gcp_service_account"]

    creds = Credentials.from_service_account_info(creds_dict)

    client = gspread.authorize(creds)

    sheet = client.open("fleet_database")

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
