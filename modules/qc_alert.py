import pandas as pd

def qc_alert(qc):

    qc_cols = [
        "BODY_DEPAN",
        "BODY_KANAN",
        "BODY_KIRI",
        "BODY_BELAKANG",
        "INTERIOR_JOK",
        "INTERIOR_KARPET",
        "INTERIOR_PLAFOND"
    ]

    # bersihkan teks
    for col in qc_cols:
        qc[col] = (
            qc[col]
            .astype(str)
            .str.strip()
            .str.upper()
        )

    # kondisi yang dianggap normal
    normal_values = ["OK", "-", "BAIK", "NORMAL"]

    # cari yang tidak normal
    mask = ~qc[qc_cols].isin(normal_values)

    alert = qc[mask.any(axis=1)]

    return alert