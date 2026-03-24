import pandas as pd

def highlight_service(row):

    km_update = pd.to_numeric(
        str(row["KM_UPDATE"]).replace(",", ""),
        errors="coerce"
    )

    km_service = pd.to_numeric(
        str(row["KM_SERVICE_NEXT"]).replace(",", ""),
        errors="coerce"
    )

    if km_update > km_service:
        return ["background-color: #ffcccc"] * len(row)

    return [""] * len(row)

def highlight_status(row):

    if row["STATUS"] == "Service Overdue":
        return ["background-color: #ffcccc"] * len(row)

    if row["STATUS"] == "Service Soon":
        return ["background-color: #fff3cd"] * len(row)

    if row["STATUS"] == "Dokumen Expired":
        return ["background-color: #f8d7da"] * len(row)

    if row["STATUS"] == "Ready":
        return ["background-color: #d4edda"] * len(row)

    return [""] * len(row)

