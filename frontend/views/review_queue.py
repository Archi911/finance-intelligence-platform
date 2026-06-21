import streamlit as st
import requests
import base64
import os

BASE_URL = "http://127.0.0.1:8000/api/v1"

# ==========================================

# STYLING

# ==========================================

st.markdown("""

<style>

.block-container{
    max-width:1400px;
    padding-top:1rem;
}

.review-card{
    border:1px solid #d1d5db;
    border-radius:16px;
    padding:20px;
    margin-bottom:15px;
}

</style>

""", unsafe_allow_html=True)

# ==========================================

# PDF VIEWER

# ==========================================

def show_pdf(pdf_path):


    if not pdf_path:
        st.warning("PDF path missing")
        return

    if not os.path.exists(pdf_path):
        st.error("PDF file not found")
        return

    with open(pdf_path, "rb") as pdf:

        base64_pdf = base64.b64encode(
            pdf.read()
        ).decode("utf-8")

    pdf_display = f"""
    <iframe
        src="data:application/pdf;base64,{base64_pdf}"
        width="100%"
        height="700"
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


    st.markdown("""
    <h1 style="font-size:50px;margin-bottom:0;">
    🔍 Human Review Center
    </h1>

    <p style="font-size:18px;color:gray;">
    AI Flagged Invoices Requiring Verification
    </p>
    """, unsafe_allow_html=True)

    try:

        response = requests.get(
            f"{BASE_URL}/review-queue"
        )

        if response.status_code != 200:

            st.error(
                f"Backend Error ({response.status_code})"
            )

            return

        reviews = response.json()

    except Exception as e:

        st.error(
            f"Unable to load review queue: {e}"
        )
        return

    if not reviews:

        st.success(
            "✅ No invoices require review"
        )
        return

# ==========================================
# KPI SECTION
# ==========================================

    pending = len(reviews)

    avg_conf = (
        sum(
            r["ocr_confidence"]
            for r in reviews
        ) / pending
        if pending else 0
    )

    high_risk = len([
        r
        for r in reviews
        if r["ocr_confidence"] < 0.5
    ])

    medium_risk = len([
        r
        for r in reviews
        if 0.5 <= r["ocr_confidence"] < 0.8
    ])

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.metric(
            "Pending Cases",
            pending
        )

    with k2:
        st.metric(
            "Average Confidence",
            f"{avg_conf*100:.0f}%"
        )

    with k3:
        st.metric(
            "High Risk",
            high_risk
        )

    with k4:
        st.metric(
            "Medium Risk",
            medium_risk
        )

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

                st.subheader(
                    f"Review Case #{review['id']}"
                )

                st.write(
                    f"📄 {review.get('file_name', 'N/A')}"
                )

                st.write(
                    f"⚠ {review['reason']}"
                )

                confidence = (
                    review.get(
                        "ocr_confidence",
                        0
                    )
                )

                st.progress(
                    confidence
                )

                st.caption(
                    f"Confidence Score: {confidence*100:.0f}%"
                )

                if confidence < 0.5:

                    st.error(
                        "🔴 HIGH RISK"
                    )

                elif confidence < 0.8:

                    st.warning(
                        "🟡 MEDIUM RISK"
                    )

                else:

                    st.success(
                        "🟢 LOW RISK"
                    )

                invoice_id = review.get(
                    "invoice_id"
                )

                if invoice_id:

                    st.info(
                        f"Invoice ID: {invoice_id}"
                    )

                else:

                    st.warning(
                        "Invoice record not created"
                    )

                st.caption(
                    review["created_at"]
                )

                # ==========================
                # AI EXTRACTED DATA
                # ==========================

                if review.get(
                    "extracted_data"
                ):

                    with st.expander(
                        "🤖 AI Extracted Data"
                    ):

                        data = review["extracted_data"]

                        st.write(
                            f"**Vendor:** {data.get('vendor_name','N/A')}"
                        )

                        st.write(
                            f"**Invoice Number:** {data.get('invoice_number','N/A')}"
                        )

                        st.write(
                            f"**Total Amount:** ₹{data.get('total_amount',0):,.2f}"
)

                # ==========================
                # ACTION BUTTONS
                # ==========================

                b1, b2 = st.columns(2)

                with b1:

                    if st.button(
                        "✅ Approve",
                        key=f"a_{review['id']}"
                    ):

                        requests.post(
                            f"{BASE_URL}/review/{review['id']}/approve"
                        )

                        st.rerun()

                with b2:

                    if st.button(
                        "❌ Reject",
                        key=f"r_{review['id']}"
                    ):

                        requests.post(
                            f"{BASE_URL}/review/{review['id']}/reject"
                        )

                        st.rerun()

            # ==================================
            # RIGHT PANEL
            # ==================================

            with right:

                with st.expander(
                    "📑 Original Invoice",
                    expanded=True
                ):

                    show_pdf(
                        review.get(
                            "pdf_path"
                        )
                    )

        st.divider()

