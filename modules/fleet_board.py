import streamlit as st
import pandas as pd

def fleet_control_board(df):

    st.subheader("🚦 Fleet Control Board")

    cols = st.columns(6)

    for i, row in df.iterrows():

        status = row["STATUS"]
        nopol = row.get("NO_POLISI", "-")
        km_update = row.get("KM_UPDATE", 0)
        km_next = row.get("KM_SERVICE_NEXT", 0)

        # =====================
        # HITUNG PROGRESS
        # =====================
        try:
            km_update = float(km_update)
            km_next = float(km_next)

            progress = km_update / km_next if km_next > 0 else 0
            progress_pct = min(int(progress * 100), 100)

        except:
            progress = 0
            progress_pct = 0

        # =====================
        # WARNA STATUS
        # =====================

        extra_info = ""
        
        if status == "Ready":
            color = "#28a745"
            icon = "🟢"

        elif status == "Service Soon":
            color = "#ffc107"
            icon = "🟡"

        elif status == "Service Overdue":
            color = "#dc3545"
            icon = "🔴"
            extra_info = f"<span style='font-size:10px;'>Over by {int(abs(km_update - km_next)):,} KM</span>"

        elif status == "Dokumen Expired":
            color = "#6c757d"
            icon = "⚫"


        # =====================
        # FORMAT ANGKA
        # =====================
        try:
            km_update_fmt = f"{int(km_update):,}"
            km_next_fmt = f"{int(km_next):,}"
        except:
            km_update_fmt = km_update
            km_next_fmt = km_next

        # =====================
        # CARD UI
        # =====================
        card = f"""
        <div style="
        background-color:{color};
        padding:14px;
        border-radius:14px;
        text-align:center;
        color:white;
        font-size:14px;
        font-weight:bold;
        margin-bottom:12px;
        ">

        {icon} {row['ID_UNIT']} <br>

        <span style="font-size:12px;">
        {nopol}
        </span>

        <br><br>

        <span style="font-size:11px;">
        {km_update_fmt} / {km_next_fmt}
        </span>

        <br>

        <!-- Progress Bar -->
        <div style="
            background-color:rgba(255,255,255,0.3);
            border-radius:10px;
            height:6px;
            margin:6px 0;
        ">
            <div style="
                width:{progress_pct}%;
                background-color:white;
                height:6px;
                border-radius:10px;
            "></div>
        </div>

        <span style="font-size:10px;">
        {progress_pct}%
        </span>

        <br>

        <span style="font-size:11px;">
        {status}
        </span>

        <br>
        {extra_info}

        </div>
        """

        cols[i % 6].markdown(card, unsafe_allow_html=True)