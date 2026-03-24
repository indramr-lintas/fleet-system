import plotly.express as px
import pandas as pd


def km_chart(km):

    fig = px.bar(
        km,
        x="ID_UNIT",
        y="KM_UPDATE",
        title="Monitoring KM Kendaraan",
        color="KM_UPDATE"
    )

    return fig


def utilization_chart(km):

    fig = px.pie(
        km,
        names="ID_UNIT",
        values="KM_UPDATE",
        title="Utilisasi Armada"
    )

    return fig


def qc_chart(qc):

    qc_status = qc[[
        "BODY_DEPAN",
        "BODY_KANAN",
        "BODY_KIRI",
        "BODY_BELAKANG"
    ]].stack().value_counts().reset_index()

    qc_status.columns = ["Status", "Total"]

    fig = px.pie(
        qc_status,
        names="Status",
        values="Total",
        title="Distribusi Status QC"
    )

    return fig