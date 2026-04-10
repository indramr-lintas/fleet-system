import streamlit as st

def qc_control_board(qc):

    st.subheader("🧰 QC Control Board")

    qc_cols = [
        "BODY_DEPAN",
        "BODY_KANAN",
        "BODY_KIRI",
        "BODY_BELAKANG",
        "INTERIOR_JOK",
        "INTERIOR_KARPET",
        "INTERIOR_PLAFOND"
    ]

    cols = st.columns(6)

    for i, row in qc.iterrows():

        issue = None

        for col in qc_cols:

            val = str(row[col]).strip().upper()

            if val not in ["OK", "-", "BAIK", "NORMAL"]:
                issue = f"{col.replace('_',' ')} {val}"
                break

        if issue is None:
            icon = "🟢"
            color = "#28a745"
            text = "OK"

        else:
            icon = "🟡"
            color = "#f7c708"
            text = issue

        card = f"""
        <div style="
        background-color:{color};
        padding:12px;
        border-radius:12px;
        text-align:center;
        color:white;
        font-size:13px;
        font-weight:bold;
        margin-bottom:10px;
        ">

        {icon} {row['ID_UNIT']} <br>

        <span style="font-size:11px;">
        {text}
        </span>

        </div>
        """

        cols[i % 6].markdown(card, unsafe_allow_html=True)