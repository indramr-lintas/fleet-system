import pandas as pd

def tire_alert(km):

    tire_cols = [
        "TWI_DEPAN_KANAN",
        "TWI_DEPAN_KIRI",
        "TWI_BLKG_KANAN",
        "TWI_BLKG_KIRI"
    ]

    for col in tire_cols:
        km[col] = pd.to_numeric(km[col], errors="coerce")

    alert = km[
        (km[tire_cols] < 2).any(axis=1)
    ]

    return alert