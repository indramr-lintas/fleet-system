import pandas as pd

def fleet_status(master, km, dokumen):

    df = master.copy()

    # gabungkan data
    df = df.merge(km[["ID_UNIT", "KM_UPDATE", "KM_SERVICE_NEXT", "SISA_KM_SERVICE"]], on="ID_UNIT", how="left")
    df = df.merge(dokumen[["ID_UNIT", "TGL_PAJAK"]], on="ID_UNIT", how="left")

    df["TGL_PAJAK"] = pd.to_datetime(df["TGL_PAJAK"], errors="coerce")

    today = pd.Timestamp.today()

    df["STATUS"] = "Ready"

    # prioritas 1
    df.loc[df["TGL_PAJAK"] < today, "STATUS"] = "Dokumen Expired"

    # prioritas 2
    df.loc[df["SISA_KM_SERVICE"] <= 0, "STATUS"] = "Service Overdue"

    # prioritas 3
    df.loc[
        (df["SISA_KM_SERVICE"] > 0) &
        (df["SISA_KM_SERVICE"] <= 1000),
        "STATUS"
    ] = "Service Soon"

    return df