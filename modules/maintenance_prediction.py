import pandas as pd

def maintenance_prediction(km):

    km["KM_UPDATE"] = pd.to_numeric(km["KM_UPDATE"], errors="coerce")
    km["KM_SERVICE_NEXT"] = pd.to_numeric(km["KM_SERVICE_NEXT"], errors="coerce")

    prediction = km[
        (km["KM_SERVICE_NEXT"] - km["KM_UPDATE"] <= 5000) &
        (km["KM_SERVICE_NEXT"] - km["KM_UPDATE"] > 0)
    ]

    prediction["SISA_KM_SERVICE"] = km["KM_SERVICE_NEXT"] - km["KM_UPDATE"]

    return prediction.sort_values("SISA_KM_SERVICE")