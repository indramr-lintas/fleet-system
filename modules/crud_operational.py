import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

def connect_sheet():

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

    return sheet

# =====================
# QC
# =====================
def create_qc(data):
    ws = connect_sheet().worksheet("QC_INSPECTION")
    ws.append_row(data)

def update_qc(row, data):
    ws = connect_sheet().worksheet("QC_INSPECTION")
    ws.update(f"A{row}:Z{row}", [data])

def delete_qc(row):
    ws = connect_sheet().worksheet("QC_INSPECTION")
    ws.delete_rows(row)

# =====================
# KM
# =====================
def create_km(data):
    ws = connect_sheet().worksheet("MONITORING_KM")
    ws.append_row(data)

def update_km(row, data):
    ws = connect_sheet().worksheet("MONITORING_KM")
    ws.update(f"A{row}:Z{row}", [data])

def delete_km(row):
    ws = connect_sheet().worksheet("MONITORING_KM")
    ws.delete_rows(row)
    