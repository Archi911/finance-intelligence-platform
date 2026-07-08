import streamlit as st
import requests
import pandas as pd

from services.api_client import BASE_URL

# ======================================================
# STYLING
# ======================================================

st.markdown("""
    <style>

    /*===========================
    GLOBAL APP
    =========================== */

    .stApp{
        background:#F8FAFC !important;
    }

    .block-container{
        max-width:1400px;
        padding-top:1rem;
        background:#F8FAFC;
    }

    /* ===========================
    SIDEBAR
    =========================== */

    [data-testid="stSidebar"]{
        background:white !important;
        border-right:1px solid #E5E7EB;
    }

    [data-testid="stSidebar"] *{
        color:#0F172A !important;
    }

    /* ===========================
    TEXT
    =========================== */

    h1,h2,h3,h4,h5,h6,
    label,p,span{
        color:#0F172A !important;
    }

    /* ===========================
    CONTAINERS
    =========================== */

    [data-testid="stVerticalBlockBorderWrapper"]{
        background:white !important;
        border:1px solid #E5E7EB !important;
        border-radius:14px;
    }

    /* ===========================
    BUTTONS
    =========================== */

    .stButton>button{
        background:white !important;
        color:#0F172A !important;
        border:1px solid #CBD5E1 !important;
    }

    .stButton>button:hover{
        border-color:#2563EB !important;
    }

    /* Primary buttons */

    button[kind="primary"]{
        background:#2563EB !important;
        color:white !important;
    }

    /* ===========================
    INPUTS
    =========================== */

    .stTextInput input,
    .stSelectbox div[data-baseweb="select"],
    .stTextArea textarea{
        background:white !important;
        color:#0F172A !important;
    }

    /* ===========================
    FILE UPLOADER
    =========================== */

    [data-testid="stFileUploader"]{
        background:white !important;
        border:1px solid #CBD5E1 !important;
        border-radius:12px;
    }

    /* ===========================
    METRICS
    =========================== */

    [data-testid="stMetricValue"]{
        color:#0F172A !important;
    }

    [data-testid="stMetricLabel"]{
        color:#64748B !important;
    }

    /* ===========================
    PROGRESS
    =========================== */

    [data-testid="stProgressBar"]{
        background:#E5E7EB;
    }

    /* ===========================
    EXPANDER
    =========================== */

    .streamlit-expanderHeader{
        color:#0F172A !important;
    }

    /* ===========================
    DATAFRAME
    =========================== */

    [data-testid="stDataFrame"]{
        background:white !important;
    }

    /* ===========================
    ALERTS
    =========================== */

    .info-danger{
        background:#FEE2E2;
        color:#991B1B;
    }

    .info-warning{
        background:#FEF3C7;
        color:#92400E;
    }

    .info-success{
        background:#DCFCE7;
        color:#166534;
    }

    </style>
    """, unsafe_allow_html=True)

def render_upload_invoice():

    # ======================================================
    # HEADER
    # ======================================================

    st.markdown("""
<div style="padding-bottom:18px; border-bottom:1px solid #E5E7EB; margin-bottom:25px;">
    <div style="font-size:34px; font-weight:700; color:#0F172A;">
        FinPilot AI
    </div>
    <div style="font-size:14px; color:#64748B; margin-top:4px;">
        Invoice Intelligence Platform
    </div>
</div>
""", unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Upload Invoice PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

    process_btn = st.button(
        "Process Invoices",
        use_container_width=True
    )

    if not process_btn:
        return

    if not uploaded_files:

        st.warning(
            "Upload at least one invoice."
        )
        return

    for file in uploaded_files:

        with st.spinner(
            f"Processing {file.name}"
        ):

            files = {
                "file": (
                    file.name,
                    file,
                    "application/pdf"
                )
            }

            response = requests.post(
                f"{BASE_URL}/ingest",
                files=files
            )

            try:
                result = response.json()

            except Exception:

                st.error(
                    f"Backend Error ({response.status_code})"
                )

                st.code(response.text)
                continue

        # ==================================================
        # APPROVED
        # ==================================================

        if result.get("status") == "approved":

            invoice = result["invoice"]

            # Wrap everything inside a bordered card
            with st.container(border=True):

                # Header with Badge (Using the exact same flexbox layout as the others)
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #E5E7EB; padding-bottom:12px; margin-bottom:12px;">
                    <div>
                        <div style="font-size:18px; font-weight:600; color:#0F172A;">{file.name}</div>
                        <div style="font-size:13px; color:#64748B;">Successfully processed and stored</div>
                    </div>
                    <div class="status-approved">Approved</div>
                </div>
                """, unsafe_allow_html=True)

                # Metrics Section 1
                c1, c2, c3, c4 = st.columns(4)

                with c1:
                    st.markdown('<div class="metric-label">Invoice ID</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-value">{result.get("invoice_id","N/A")}</div>', unsafe_allow_html=True)

                with c2:
                    st.markdown('<div class="metric-label">Vendor</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-value">{invoice["vendor_name"]}</div>', unsafe_allow_html=True)

                with c3:
                    st.markdown('<div class="metric-label">Total Amount</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-value">₹{invoice["total_amount"]:,.0f}</div>', unsafe_allow_html=True)

                with c4:
                    st.markdown('<div class="metric-label">Confidence</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-value">{result["confidence_score"]*100:.0f}%</div>', unsafe_allow_html=True)

                st.write("")

                # Metrics Section 2
                c1, c2, c3 = st.columns(3)
                subtotal = invoice["total_amount"] - invoice["gst_amount"]
                
                with c1:
                    st.markdown('<div class="metric-label">Subtotal</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-value">₹{subtotal:,.2f}</div>', unsafe_allow_html=True)

                with c2:
                    st.markdown('<div class="metric-label">GST Amount</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-value">₹{invoice["gst_amount"]:,.2f}</div>', unsafe_allow_html=True)

                with c3:
                    st.markdown('<div class="metric-label">Grand Total</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-value">₹{invoice["total_amount"]:,.2f}</div>', unsafe_allow_html=True)

                st.write("")

                # Line Items Table
                st.markdown('<div class="section-title">Line Items</div>', unsafe_allow_html=True)

                st.dataframe(
                    pd.DataFrame(invoice["line_items"]),
                    use_container_width=True,
                    hide_index=True
                )

                with st.expander("View Extracted JSON"):
                    st.json(invoice)

            st.write("")


        elif result.get("status") == "duplicate":

            st.info(
                "Invoice already exists in the system"
            )

            st.metric(
                "Existing Invoice ID",
                result["invoice_id"]
            )

            st.caption(
                "Duplicate invoice detected. No new record was created."
            )

        # ==================================================
        # REVIEW REQUIRED
        # ==================================================

        elif result.get("status") == "review_required":

            # Wrap everything inside a bordered card
            with st.container(border=True):

                # Header with Badge
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #E5E7EB; padding-bottom:12px; margin-bottom:12px;">
                    <div>
                        <div style="font-size:18px; font-weight:600; color:#0F172A;">{file.name}</div>
                        <div style="font-size:13px; color:#64748B;">Manual verification required</div>
                    </div>
                    <div class="status-review">Review Required</div>
                </div>
                """, unsafe_allow_html=True)

                # Metrics
                c1, c2, c3 = st.columns(3)

                with c1:
                    st.markdown('<div class="metric-label">Review Case</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-value">{result["review_id"]}</div>', unsafe_allow_html=True)

                with c2:
                    st.markdown('<div class="metric-label">Confidence</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-value">{result["confidence_score"]*100:.0f}%</div>', unsafe_allow_html=True)

                with c3:
                    st.markdown('<div class="metric-label">Risk Score</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-value">{100-result["confidence_score"]*100:.0f}%</div>', unsafe_allow_html=True)

                st.write("")
                st.progress(result["confidence_score"])
                
                # Replaced the yellow st.warning() bar with clean, subtle text
                st.markdown(f'<div style="font-size:13px; color:#92400E; margin-top:8px;"><strong>Reason for review:</strong> {result["reason"]}</div>', unsafe_allow_html=True)

                st.write("")

                with st.expander("View Backend Response"):
                    st.json(result)

            st.write("")