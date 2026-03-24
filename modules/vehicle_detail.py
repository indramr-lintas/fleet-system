import streamlit as st

def vehicle_detail(master, km, dokumen, qc, unit):

    st.subheader(f"🚐 Detail Kendaraan : {unit}")

    master_unit = master[master["ID_UNIT"] == unit]
    km_unit = km[km["ID_UNIT"] == unit]
    dok_unit = dokumen[dokumen["ID_UNIT"] == unit]
    qc_unit = qc[qc["ID_UNIT"] == unit]

    # =====================
    # DATA KENDARAAN
    # =====================

    st.markdown("### Data Kendaraan")

    if not master_unit.empty:

        row = master_unit.iloc[0]

        col1, col2 = st.columns(2)

        col1.write(f"Jenis Kendaraan : {row.get('JENIS_KENDARAAN','-')}")
        

        col2.write(f"No Polisi : {row.get('NO_POLISI','-')}")
        col2.write(f"Tahun : {row.get('TAHUN','-')}")
      # col2.write(f"No Body : {row.get('NO_BODY','-')}")

    # =====================
    # KM MONITORING
    # =====================

    st.markdown("### KM Monitoring")

    if not km_unit.empty:

        row = km_unit.iloc[0]

        col1, col2 = st.columns(2)

        col1.metric("KM Update", row.get("KM_UPDATE","-"))
        col2.metric("Next Service", row.get("KM_SERVICE_NEXT","-"))

    # =====================
    # DOKUMEN
    # =====================

    st.markdown("### Dokumen Kendaraan")

    if not dok_unit.empty:

        row = dok_unit.iloc[0]

        col1, col2, col3 = st.columns(3)

        col1.write(f"STNK : {row.get('TGL_STNK','-')}")
        col2.write(f"PAJAK : {row.get('TGL_PAJAK','-')}")
        col3.write(f"KIR : {row.get('TGL_KIR','-')}")

    # =====================
    # QC
    # =====================

    st.markdown("### QC Condition")

    if not qc_unit.empty:

        st.dataframe(qc_unit, use_container_width=True)