import pandas as pd

def fleet_status(master, km, dokumen):

    df = master.copy()

    # merge data
    df = df.merge(
        km[["ID_UNIT", "KM_UPDATE", "KM_SERVICE_NEXT"]],
        on="ID_UNIT",
        how="left"
    )

    df = df.merge(
        dokumen[["ID_UNIT", "TGL_PAJAK"]],
        on="ID_UNIT",
        how="left"
    )

    # convert
    df["KM_UPDATE"] = (
    df["KM_UPDATE"]
    .astype(str)
    .str.replace(".", "", regex=False)
    )

    df["KM_SERVICE_NEXT"] = (
        df["KM_SERVICE_NEXT"]
        .astype(str)
        .str.replace(".", "", regex=False)
    )

    df["KM_UPDATE"] = pd.to_numeric(df["KM_UPDATE"], errors="coerce")
    df["KM_SERVICE_NEXT"] = pd.to_numeric(df["KM_SERVICE_NEXT"], errors="coerce")
    df["TGL_PAJAK"] = pd.to_datetime(df["TGL_PAJAK"], errors="coerce")
    
    # hitung sisa km
    df["SISA_KM_SERVICE"] = df["KM_SERVICE_NEXT"] - df["KM_UPDATE"]

    today = pd.Timestamp.today()

    # default
    df["STATUS"] = "Ready"

    # 🔴 PRIORITAS 1: dokumen expired
    df.loc[df["TGL_PAJAK"] < today, "STATUS"] = "Dokumen Expired"

    # 🔴 PRIORITAS 2: service overdue
    df.loc[df["SISA_KM_SERVICE"] < 0, "STATUS"] = "Service Overdue"

    # 🟡 PRIORITAS 3: service soon
    df.loc[
        (df["SISA_KM_SERVICE"] >= 0) &
        (df["SISA_KM_SERVICE"] <= 1000),
        "STATUS"
    ] = "Service Soon"

    return df