import streamlit as st
from PIL import Image
import os
import adk_agent

st.set_page_config(page_title="OmniRelay AI (GCP Cloud Shell)", layout="wide", page_icon="📦")

st.sidebar.title("🛠️ Project Details")
st.sidebar.markdown("""
- **Environment:** GCP Cloud Shell
- **Framework:** Google ADK (`google-adk`)
- **Model:** Google Gemini Flash
- **Tools:** FastMCP (Model Context Protocol)
- **Feedback Loop:** Evaluator-Optimizer Critic
""")
st.sidebar.divider()
st.sidebar.code("Hubs: HUB-DOWNTOWN-01, HUB-METRO-EAST\nSKUs: SKU-PWR-65W, SKU-ANC-HEADSET")

# Modal dialog comparing the initial plan vs corrected plan + interactive chat
@st.dialog("🔄 Autonomous Feedback Loop & Conversational Audit Review", width="large")
def show_feedback_modal(res: dict):
    badge = "green" if res["status"] == "APPROVED" else "orange"
    st.markdown(f"### Overall Audit Verdict: :{badge}[{res['status']}]")
    
    with st.expander("🔍 View Policy Audit JSON Telemetry", expanded=False):
        st.json(res["audit"])

    # Side-by-side comparison
    col_initial, col_corrected = st.columns(2)
    with col_initial:
        st.markdown("#### 📋 Initial Action Plan")
        st.info(res["dispatch_plan"])

    with col_corrected:
        st.markdown("#### ⚡ Self-Corrected Action Plan")
        if res["status"] == "REFINED_VIA_FEEDBACK_LOOP":
            st.success(res["final_plan"])
        else:
            st.success("✅ Plan passed all constraints with zero remediation required.")
            st.info(res["final_plan"])

    st.markdown("---")
    st.markdown("#### 💬 Converse with Agent on this Audit")

    # Initialize chat history for the dialog in session_state
    if "dialog_messages" not in st.session_state:
        st.session_state.dialog_messages = []

    # Display past conversation in the modal
    for message in st.session_state.dialog_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input inside the dialog
    user_input = st.chat_input("Ask why a rule failed, request adjustments, or ask for phased shipment...")
    if user_input:
        st.session_state.dialog_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing plan context..."):
                reply = adk_agent.chat_with_audit_context(
                    st.session_state.dialog_messages[:-1], 
                    res, 
                    user_input
                )
                st.markdown(reply)
                st.session_state.dialog_messages.append({"role": "assistant", "content": reply})

st.title("📦 OmniRelay AI: Autonomous Supply Chain Agent")
st.caption("Running directly inside GCP Cloud Shell using Google ADK & FastMCP")

col1, col2 = st.columns(2)

with col1:
    st.subheader("💬 Google ADK Dispatch & Feedback Loop")
    query = st.text_area(
        "Agent Prompt:",
        "We have an urgent enterprise demand surge. Dispatch 150 units of SKU-SSD-1TB to HUB-METRO-EAST immediately."
    )
    if st.button("Execute ADK Workflow", type="primary"):
        st.session_state.dialog_messages = []
        with st.spinner("ADK Agents running tools and risk audit..."):
            res = adk_agent.run_adk_workflow(query)
            show_feedback_modal(res)

with col2:
    st.subheader("👁️ Multimodal Cargo & Tamper Inspection")
    file = st.file_uploader("Upload Box / Seal Image", type=["jpg", "png", "jpeg"])
    note = st.text_input("Inspector Note", value="Return box received with torn corner tape.")
    if file:
        img = Image.open(file)
        st.image(img, use_container_width=True)
        if st.button("Inspect Cargo"):
            with st.spinner("Gemini Multimodal analyzing..."):
                report = adk_agent.inspect_cargo_tampering(img, note)
                st.markdown("### 📋 QA Verdict")
                st.write(report)
