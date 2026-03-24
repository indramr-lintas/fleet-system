import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

#FILE = "data/fleet_management_template.xlsx"

def load_data():

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "fleet-system-491104-112c658e4fb2.json", scope
    )

    client = gspread.authorize(creds)

    sheet = client.open("fleet_database")

    
    master = pd.DataFrame(sheet.worksheet("MASTER_KENDARAAN").get_all_records())
    dokumen = pd.DataFrame(sheet.worksheet("DOKUMEN_KENDARAAN").get_all_records())
    km = pd.DataFrame(sheet.worksheet("MONITORING_KM").get_all_records())
    qc = pd.DataFrame(sheet.worksheet("QC_INSPECTION").get_all_records())

    #master = pd.read_excel(FILE, sheet_name="MASTER_KENDARAAN")
    #dokumen = pd.read_excel(FILE, sheet_name="DOKUMEN_KENDARAAN")
    #km = pd.read_excel(FILE, sheet_name="MONITORING_KM")
    #qc = pd.read_excel(FILE, sheet_name="QC_INSPECTION")

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


