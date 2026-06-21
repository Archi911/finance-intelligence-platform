import streamlit as st

from views.dashboard import render_dashboard
from views.upload_invoice import render_upload_invoice
from views.review_queue import render_review_queue
from views.exxport_data import render_export_data

st.set_page_config(
    page_title="CogniPay AI",
    page_icon="🤖",
    layout="wide"
)

page = st.sidebar.selectbox(
    "Navigation",
    [
        "Analytics Copilot",
        "Upload Invoice",
        "Review Queue",
        "Export Data"
    ]
)

if page == "Analytics Copilot":
    render_dashboard()

elif page == "Upload Invoice":
    render_upload_invoice()

elif page == "Review Queue":
    render_review_queue()

elif page == "Export Data":
    render_export_data()