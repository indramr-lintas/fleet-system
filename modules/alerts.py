import pandas as pd


def service_alert(km):

    km["KM_UPDATE"] = pd.to_numeric(
        km["KM_UPDATE"].astype(str).str.replace(",", ""),
        errors="coerce"
    )

    km["KM_SERVICE_NEXT"] = pd.to_numeric(
        km["KM_SERVICE_NEXT"].astype(str).str.replace(",", ""),
        errors="coerce"
    )

    alert = km[km["KM_UPDATE"] > km["KM_SERVICE_NEXT"]]

    return alert


def document_alert(dokumen):

    today = pd.Timestamp.today()

    dokumen["TGL_PAJAK"] = pd.to_datetime(
        dokumen["TGL_PAJAK"],
        errors="coerce"
    )

    alert = dokumen[dokumen["TGL_PAJAK"] < today]

    return alert