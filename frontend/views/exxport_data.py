import streamlit as st
import pandas as pd
import requests

from services.api_client import BASE_URL

# ==========================================
# STYLING
# ==========================================

st.markdown("""
<style>

.block-container{
    max-width:1200px;
    padding-top:1rem;
}

.info-box {
    font-size:13px; 
    padding:8px 12px; 
    border-radius:6px; 
    margin-bottom:12px;
}
.info-success { background:#DCFCE7; color:#166534; border-left: 3px solid #22C55E; }

</style>
""", unsafe_allow_html=True)

def render_export_data():

    # ======================================================
    # HEADER
    # ======================================================

    st.markdown("""
    <div style="padding-bottom:18px; border-bottom:1px solid #E5E7EB; margin-bottom:25px;">
        <div style="font-size:34px; font-weight:700; color:#0F172A;">
            Data Export Center
        </div>
        <div style="font-size:14px; color:#64748B; margin-top:4px;">
            Download consolidated invoice records for ERP integration
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ======================================================
    # EXPORT CARD
    # ======================================================

    with st.container(border=True):

        left, right = st.columns([3, 1], gap="large")

        with left:
            st.markdown('<div style="font-size:18px; font-weight:600; color:#0F172A; margin-bottom:4px;">Full Database Export</div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:13px; color:#64748B; margin-bottom:16px;">Compile all processed, approved, and rejected invoice data into a standard CSV format. Depending on database size, this may take a moment.</div>', unsafe_allow_html=True)

        with right:
            
            # Step 1: Fetch and compile the data into session state
            if st.button("Prepare Export File", use_container_width=True):
                
                with st.spinner("Compiling database..."):
                    try:
                        response = requests.get(f"{BASE_URL}/export-all")
                        
                        if response.status_code == 200:
                            data = response.json().get("data", [])
                            
                            if data:
                                df = pd.DataFrame(data)
                                st.session_state["export_csv"] = df.to_csv(index=False)
                            else:
                                st.warning("No records found in database.")
                        else:
                            st.error(f"Backend Error ({response.status_code})")
                            
                    except Exception as e:
                        st.error(f"Connection failed: {e}")

            # Step 2: Show the actual download button once the data is ready
            if "export_csv" in st.session_state:
                
                st.markdown('<div class="info-box info-success">File ready for download</div>', unsafe_allow_html=True)
                
                st.download_button(
                    label="Download CSV",
                    data=st.session_state["export_csv"],
                    file_name="cognipay_all_invoices.csv",
                    mime="text/csv",
                    type="primary", # Makes the button blue/accent color
                    use_container_width=True
                )

    # Add a bit of spacing at the bottom
    st.write("")