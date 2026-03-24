import pandas as pd


def fleet_status(master, km, dokumen):

    df = master.copy()

    # gabungkan data
    df = df.merge(km[["ID_UNIT", "KM_UPDATE", "KM_SERVICE_NEXT"]], on="ID_UNIT", how="left")
    df = df.merge(dokumen[["ID_UNIT", "TGL_PAJAK"]], on="ID_UNIT", how="left")

    # konversi data
    df["KM_UPDATE"] = pd.to_numeric(df["KM_UPDATE"], errors="coerce")
    df["KM_SERVICE_NEXT"] = pd.to_numeric(df["KM_SERVICE_NEXT"], errors="coerce")

    df["TGL_PAJAK"] = pd.to_datetime(df["TGL_PAJAK"], errors="coerce")

    today = pd.Timestamp.today()

    status = []

    for _, row in df.iterrows():

        if row["TGL_PAJAK"] < today:
            status.append("Dokumen Expired")

        elif row["KM_UPDATE"] > row["KM_SERVICE_NEXT"]:
            status.append("Service Overdue")

        elif row["KM_SERVICE_NEXT"] - row["KM_UPDATE"] < 2000:
            status.append("Service Soon")

        else:
            status.append("Ready")

    df["STATUS"] = status

    return df