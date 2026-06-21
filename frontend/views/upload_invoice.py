import streamlit as st
import requests
import pandas as pd
st.markdown("""
<style>

.block-container{
    max-width:1400px;
    padding-top:1rem;
}

.main-card{
    padding:20px;
    border-radius:18px;
    border:1px solid #e5e7eb;
    background:#fafafa;
    margin-bottom:15px;
}

.metric-box{
    padding:15px;
    border-radius:12px;
    background:#111827;
    color:white;
}

.status-approved{
    padding:15px;
    border-radius:12px;
    background:#dcfce7;
    color:#166534;
}

.status-review{
    padding:15px;
    border-radius:12px;
    background:#fef3c7;
    color:#92400e;
}

.review-card{
    border:1px solid #d1d5db;
    border-radius:16px;
    padding:20px;
    margin-bottom:15px;
}

</style>
""", unsafe_allow_html=True)

def render_upload_invoice():

    st.markdown("""
        <h1 style="font-size:52px;margin-bottom:0;">
        🤖 CogniPay AI
        </h1>

        <p style="font-size:18px;color:gray;">
        Enterprise Invoice Intelligence Platform
        </p>
        """, unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Upload Invoice PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

    if st.button(
        "🚀 Process Invoice",
        use_container_width=True
    ):

        if not uploaded_files:

            st.warning(
                "Please upload at least one invoice."
            )
            return

        for file in uploaded_files:

            with st.spinner(
                f"Processing {file.name}..."
            ):

                files = {
                    "file": (
                        file.name,
                        file,
                        "application/pdf"
                    )
                }

                response = requests.post(
                    "http://127.0.0.1:8000/api/v1/ingest",
                    files=files
                )

                try:
                    result = response.json()

                except Exception:

                    st.error(
                        f"Backend Error ({response.status_code})"
                    )

                    st.code(
                        response.text
                    )

                    continue

            st.divider()

            st.subheader(
                f"📄 {file.name}"
            )

            # ==================================
            # APPROVED
            # ==================================

            if result.get("status") == "approved":

                invoice = result["invoice"]

                st.success(
                    "✅ Invoice Approved & Stored"
                )

                c1,c2,c3,c4 = st.columns(4)

                with c1:
                    st.metric(
                        "Invoice ID",
                        result.get("invoice_id", "N/A")
                    )

                with c2:
                    st.metric(
                        "Vendor",
                        invoice["vendor_name"]
                    )

                with c3:
                    st.metric(
                        "Total Amount",
                        f"₹{invoice['total_amount']:,.0f}"
                    )

                with c4:
                    st.metric(
                        "Confidence",
                        f"{result['confidence_score']*100:.0f}%"
                    )

                st.progress(
                    result["confidence_score"]
                )
                st.divider()

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "GST Amount",
                        f"₹{invoice['gst_amount']:,.2f}"
                    )

                with col2:

                    st.metric(
                        "Total Amount",
                        f"₹{invoice['total_amount']:,.2f}"
                    )

                st.subheader(
                    "📦 Line Items"
                )

                st.dataframe(
                    pd.DataFrame(
                        invoice["line_items"]
                    ),
                    use_container_width=True
                )

                with st.expander(
                    "🔍 Extracted JSON"
                ):
                    st.json(invoice)

            # ==================================
            # REVIEW QUEUE
            # ==================================

            elif result.get("status") == "review_required":

                st.warning(
                    "⚠ Invoice Routed For Human Review"
                )

                c1,c2,c3 = st.columns(3)

                with c1:
                    st.metric(
                        "Review Case",
                        result["review_id"]
                    )

                with c2:
                    st.metric(
                        "Confidence",
                        f"{result['confidence_score']*100:.0f}%"
                    )

                with c3:
                    st.metric(
                        "Risk Score",
                        f"{100-result['confidence_score']*100:.0f}%"
                    )

                st.progress(
                    result.get("confidence_score", 0)
                )

                st.error(
                    result["reason"]
                )

                with st.expander(
                    "View Backend Response"
                ):
                    st.json(result)

            else:

                st.error(
                    "Unexpected response received."
                )

                st.json(result)