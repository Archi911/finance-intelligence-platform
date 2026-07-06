import streamlit as st
import pandas as pd

from backend.app.services.api_client import (
    ask_question,
    get_dashboard_metrics
)

# ======================================================
# GLOBAL STYLES
# ======================================================

st.markdown("""
<style>

.block-container{
    max-width:1100px;
    padding-top:0.5rem;
}

body{
    background:#F8FAFC;
}

.header-card{
    background:white;
    border:1px solid #E5E7EB;
    border-radius:16px;
    padding:24px;
    margin-bottom:20px;
}

.metric-card{
    background:white;
    border:1px solid #E5E7EB;
    border-radius:12px;
    padding:14px;
}

.metric-label{
    color:#64748B;
    font-size:13px;
}

.metric-value{
    color:#0F172A;
    font-size:18px;
    font-weight:600;
}

.copilot-card{
    background:white;
    border:1px solid #E5E7EB;
    border-radius:16px;
    padding:20px;
}

.section-title{
    font-size:18px;
    font-weight:600;
    color:#0F172A;
}

.small-muted{
    color:#64748B;
    font-size:14px;
}

</style>
""", unsafe_allow_html=True)


def metric_card(title, value):

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{title}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def render_dashboard():

    # ==========================================
    # HEADER
    # ==========================================

    st.markdown("""
    <div style="
    padding-bottom:18px;
    border-bottom:1px solid #E5E7EB;
    margin-bottom:25px;
    ">

    <div style="
    font-size:34px;
    font-weight:700;
    color:#0F172A;
    ">
    FinPilot AI
    </div>

    <div style="
    font-size:14px;
    color:#64748B;
    margin-top:5px;
    ">
    Accounts Payable Intelligence Platform
    </div>

    </div>
    """, unsafe_allow_html=True)

    # ==========================================
    # SIDEBAR
    # ==========================================

    st.sidebar.markdown("### Platform")

    st.sidebar.markdown("""
##### Workflow

1. OCR Processing
2. AI Extraction
3. Validation
4. Data Storage
5. Analytics Layer
""")

    if st.sidebar.button(
        "Clear Conversation",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

    # ==========================================
    # METRICS
    # ==========================================

    try:

        metrics = get_dashboard_metrics()

        c1,c2,c3,c4 = st.columns(4)

        with c1:
            metric_card(
                "Invoices",
                metrics["invoices"]
            )

        with c2:
            metric_card(
                "Vendors",
                metrics["vendors"]
            )

        with c3:
            metric_card(
                "GST Captured",
                f"₹{metrics['gst']:,.0f}"
            )

        with c4:
            metric_card(
                "Total Spend",
                f"₹{metrics['spend']:,.0f}"
            )

    except Exception as e:

        st.warning(
            f"Unable to load metrics: {e}"
        )

    st.write("")

    # ==========================================
    # COPILOT
    # ==========================================

    st.markdown("""
    <div style="
    font-size:18px;
    font-weight:600;
    color:#0F172A;
    margin-bottom:4px;
    ">
    Finance Analytics Copilot
    </div>

    <div style="
    font-size:14px;
    color:#64748B;
    margin-bottom:20px;
    ">
    Query invoices, vendors, GST, spending trends and financial operations.
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # ==========================================
    # CHAT HISTORY
    # ==========================================

    for msg in st.session_state.messages:

        if msg["role"] == "user":

            st.markdown(
                f"""
                <div style="
                background:#F8FAFC;
                border:1px solid #E5E7EB;
                border-radius:12px;
                padding:16px;
                margin-bottom:12px;
                ">
                    <div style="
                    color:#0F172A;
                    font-size:15px;
                    ">
                        {msg["content"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            answer = msg.get("answer", "")

            st.markdown(
                f"""
                <div style="
                background:white;
                border:1px solid #E5E7EB;
                border-radius:12px;
                padding:18px;
                margin-bottom:12px;
                box-shadow:0 1px 2px rgba(0,0,0,.04);
                ">

                    <div style="
                    color:#0F172A;
                    font-size:15px;
                    line-height:1.8;
                    ">
                    {answer}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            insights = msg.get("insights", [])

            if insights:

                st.markdown(
                    """
                    <div style="
                    margin-top:-4px;
                    margin-bottom:12px;
                    padding-left:10px;
                    ">
                    """,
                    unsafe_allow_html=True
                )

                for insight in insights:

                    st.caption(insight)

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )

        if "chart" in msg:

            st.bar_chart(msg["chart"])

        if "csv" in msg:

            st.download_button(
                "Export Data",
                data=msg["csv"],
                file_name="analytics.csv",
                mime="text/csv"
            )

        if "sql" in msg:

            with st.expander("View Query"):

                st.code(
                    msg["sql"],
                    language="sql"
                )

    # ==========================================
    # USER QUESTION
    # ==========================================

    question = st.chat_input(
        "Ask finance questions..."
    )

    if question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        try:

            response = ask_question(
                question
            )

            answer = response.get(
                "answer",
                "No answer generated."
            )

            insights = response.get(
                "insights",
                []
            )

            assistant_message = {
                "role": "assistant",
                "answer": answer,
                "insights": insights
            }


            if (
                response.get(
                    "visualization"
                )
                == "bar_chart"
            ):

                try:

                    df = pd.DataFrame(
                        response["data"],
                        columns=[
                            "Vendor",
                            "Amount"
                        ]
                    )

                    assistant_message[
                        "chart"
                    ] = df.set_index(
                        "Vendor"
                    )

                except:
                    pass

            if "data" in response:

                try:

                    df = pd.DataFrame(
                        response["data"]
                    )

                    assistant_message[
                        "csv"
                    ] = df.to_csv(
                        index=False
                    )

                except:
                    pass

            if "sql" in response:

                assistant_message[
                    "sql"
                ] = response["sql"]

            st.session_state.messages.append(
                assistant_message
            )

        except Exception as e:

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "answer": f"Error: {str(e)}",
                    "insights": []
                }
            )

        st.rerun()