import streamlit as st
import requests
import base64
import os

from services.api_client import BASE_URL

# ==========================================
# STYLING
# ==========================================

st.markdown("""
<style>

.block-container{
    max-width:1400px;
    padding-top:1rem;
}

/* Normalize KPI Metrics */
[data-testid="stMetricValue"] > div {
    font-size: 24px !important; 
    font-weight: 600 !important;
    color: #0F172A !important;
}

[data-testid="stMetricLabel"] > label {
    font-size: 13px !important;
    color: #64748B !important;
    margin-bottom: 2px !important;
}

/* Custom Badges */
.risk-badge {
    padding: 4px 8px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.risk-high { background: #FEE2E2; color: #991B1B; }
.risk-medium { background: #FEF3C7; color: #92400E; }
.risk-low { background: #DCFCE7; color: #166534; }

.info-box {
    font-size:13px; 
    padding:8px 12px; 
    border-radius:6px; 
    margin-bottom:12px;
}
.info-danger { background:#FEE2E2; color:#991B1B; border-left: 3px solid #EF4444; }
.info-warning { background:#FEF3C7; color:#92400E; }
.info-success { background:#DCFCE7; color:#166534; }

</style>
""", unsafe_allow_html=True)

# ==========================================
# PDF VIEWER
# ==========================================

def show_pdf(pdf_path):

    if not pdf_path:

        st.markdown(
            '<div class="info-box info-warning">PDF path missing</div>',
            unsafe_allow_html=True
        )
        return

    # Fix relative path from backend
    if not os.path.exists(pdf_path):

        fixed_path = os.path.join(
            "backend",
            "app",
            pdf_path
        )

        if os.path.exists(fixed_path):
            pdf_path = fixed_path

    if not os.path.exists(pdf_path):

        st.markdown(
            f'<div class="info-box info-danger">PDF file not found:<br>{pdf_path}</div>',
            unsafe_allow_html=True
        )
        return

    with open(pdf_path, "rb") as pdf:

        base64_pdf = (
            base64.b64encode(
                pdf.read()
            ).decode("utf-8")
        )

    pdf_display = f"""
    <iframe
        src="data:application/pdf;base64,{base64_pdf}"
        width="100%"
        height="800"
        type="application/pdf">
    </iframe>
    """

    st.markdown(
        pdf_display,
        unsafe_allow_html=True
    )

# ==========================================
# REVIEW QUEUE PAGE
# ==========================================

def render_review_queue():

    # Clean Header
    st.markdown("""
    <div style="padding-bottom:18px; border-bottom:1px solid #E5E7EB; margin-bottom:25px;">
        <div style="font-size:34px; font-weight:700; color:#0F172A;">
            Human Review Center
        </div>
        <div style="font-size:14px; color:#64748B; margin-top:4px;">
            AI Flagged Invoices Requiring Verification
        </div>
    </div>
    """, unsafe_allow_html=True)

    try:
        response = requests.get(f"{BASE_URL}/review-queue")

        if response.status_code != 200:
            st.error(f"Backend Error ({response.status_code})")
            return

        reviews = response.json()

    except Exception as e:
        st.error(f"Unable to load review queue: {e}")
        return

    if not reviews:
        st.success("All caught up! No invoices require review.")
        return

    # ==========================================
    # KPI SECTION
    # ==========================================

    pending = len(reviews)
    avg_conf = sum(r["ocr_confidence"] for r in reviews) / pending if pending else 0
    high_risk = len([r for r in reviews if r["ocr_confidence"] < 0.5])
    medium_risk = len([r for r in reviews if 0.5 <= r["ocr_confidence"] < 0.8])

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.metric("Pending Cases", pending)
    with k2:
        st.metric("Average Confidence", f"{avg_conf*100:.0f}%")
    with k3:
        st.metric("High Risk", high_risk)
    with k4:
        st.metric("Medium Risk", medium_risk)

    st.divider()

    # ==========================================
    # REVIEW CARDS
    # ==========================================

    for review in reviews:

        with st.container(border=True):

            left, right = st.columns([2, 3])

            # ==================================
            # LEFT PANEL
            # ==================================

            with left:

                st.markdown(f'<div style="font-size:18px; font-weight:600; color:#0F172A; margin-bottom:4px;">Review Case #{review["id"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="font-size:13px; color:#64748B; margin-bottom:16px;">File: {review.get("file_name", "N/A")}</div>', unsafe_allow_html=True)

                st.markdown(f'<div class="info-box info-danger"><strong>Flagged:</strong> {review["reason"]}</div>', unsafe_allow_html=True)

                confidence = review.get("ocr_confidence", 0)

                # Determine Risk Badge
                if confidence < 0.5:
                    risk_html = '<span class="risk-badge risk-high">High Risk</span>'
                elif confidence < 0.8:
                    risk_html = '<span class="risk-badge risk-medium">Medium Risk</span>'
                else:
                    risk_html = '<span class="risk-badge risk-low">Low Risk</span>'

                # Confidence Header & Progress
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px; margin-top:16px;">
                    <span style="font-size:13px; font-weight:600; color:#475569;">Confidence Score: {confidence*100:.0f}%</span>
                    {risk_html}
                </div>
                """, unsafe_allow_html=True)
                
                st.progress(confidence)

                # Invoice Record Status
                invoice_id = review.get("invoice_id")
                st.write("")
                if invoice_id:
                    st.markdown(f'<div class="info-box info-success" style="margin-top:8px;">Linked Invoice ID: {invoice_id}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="info-box info-warning" style="margin-top:8px;">Invoice record not yet created</div>', unsafe_allow_html=True)

                st.markdown(f'<div style="font-size:11px; color:#94A3B8; margin-bottom:16px;">Timestamp: {review["created_at"]}</div>', unsafe_allow_html=True)

                # ==========================
                # AI EXTRACTED DATA
                # ==========================

                if review.get("extracted_data"):
                    with st.expander("Extracted Data Details"):
                        data = review["extracted_data"]
                        st.markdown(f"""
                        <div style="font-size:13px; color:#334155;">
                            <div style="margin-bottom:6px;"><strong>Vendor:</strong> {data.get('vendor_name','N/A')}</div>
                            <div style="margin-bottom:6px;"><strong>Invoice Number:</strong> {data.get('invoice_number','N/A')}</div>
                            <div><strong>Total Amount:</strong> ₹{data.get('total_amount',0):,.2f}</div>
                        </div>
                        """, unsafe_allow_html=True)

                st.write("")

                # ==========================
                # ACTION BUTTONS
                # ==========================

                b1, b2 = st.columns(2)

                with b1:
                    if st.button("Approve", type="primary", use_container_width=True, key=f"a_{review['id']}"):
                        requests.post(f"{BASE_URL}/review/{review['id']}/approve")
                        st.rerun()

                with b2:
                    if st.button("Reject", use_container_width=True, key=f"r_{review['id']}"):
                        requests.post(f"{BASE_URL}/review/{review['id']}/reject")
                        st.rerun()

            # ==================================
            # RIGHT PANEL
            # ==================================

            with right:
                with st.expander("Original Invoice Document", expanded=True):
                    show_pdf(review.get("pdf_path"))

        st.divider()