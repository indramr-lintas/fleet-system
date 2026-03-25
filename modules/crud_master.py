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

    return sheet.worksheet("MASTER_KENDARAAN")


# =====================
# CREATE
# =====================
def create_master(id_unit, no_polisi):

    ws = connect_sheet()

    ws.append_row([id_unit, no_polisi])


# =====================
# UPDATE
# =====================
def update_master(row_index, id_unit, no_polisi):

    ws = connect_sheet()

    ws.update(f"A{row_index}:B{row_index}", [[id_unit, no_polisi]])


# =====================
# DELETE
# =====================
def delete_master(row_index):

    ws = connect_sheet()

    ws.delete_rows(row_index)