import streamlit as st
import pandas as pd
import requests

def render_export_data():


    st.header(
        "📤 Export Invoice Data"
    )

    if st.button(
        "Download Entire Database"
    ):

        response = requests.get(
            "http://127.0.0.1:8000/api/v1/export-all"
        )

        data = response.json()["data"]

        df = pd.DataFrame(
            data
        )

        csv = df.to_csv(
            index=False
        )

        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="all_invoices.csv",
            mime="text/csv"
        )
