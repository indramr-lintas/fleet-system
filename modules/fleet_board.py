import streamlit as st
import pandas as pd


def fleet_control_board(df):

    st.subheader("🚦 Fleet Control Board")

    cols = st.columns(6)

    for i, row in df.iterrows():

        status = row["STATUS"]

        nopol = row.get("NO POLISI", "-")
        km = row.get("KM_UPDATE", "-")

        if status == "Ready":
            color = "#28a745"
            icon = "🟢"

        elif status == "Service Soon":
            color = "#ffc107"
            icon = "🟡"

        else:
            color = "#dc3545"
            icon = "🔴"

        card = f"""
        <div style="
        background-color:{color};
        padding:12px;
        border-radius:12px;
        text-align:center;
        color:white;
        font-size:14px;
        font-weight:bold;
        margin-bottom:10px;
        ">

        {icon} {row['ID_UNIT']} <br>

        <span style="font-size:12px;">
        {nopol}
        </span>

        <br>

        <span style="font-size:11px;">
        KM {km}
        </span>

        <br>

        <span style="font-size:11px;">
        {status}
        </span>

        </div>
        """

        cols[i % 6].markdown(card, unsafe_allow_html=True)