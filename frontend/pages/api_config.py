import streamlit as st
from frontend.components.cards import render_card


def render_api_config_page() -> None:
    """
    Renders the Aeterna API Configuration Page for securely managing API keys.
    """
    # Page Header
    st.markdown("""
    <div style="padding: 20px 0;">
        <div class="dashboard-title">🔑 API Configuration</div>
        <div class="dashboard-subtitle">Securely connect Aeterna to your AI services</div>
    </div>
    """, unsafe_allow_html=True)

    # Gemini API Key Section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        render_card(
            title="Gemini API Configuration",
            body="Enter your Gemini API key to enable AI-powered features in Aeterna."
        )
        
        # API Key Input
        api_key = st.text_input(
            "Enter your Gemini API Key",
            type="password",
            placeholder="Enter your Gemini API Key",
            value=st.session_state.get("gemini_api_key", ""),
            help="Your API key is stored only in your session and never saved permanently"
        )
        
        # Validate Key Button
        if st.button("Validate API Key", type="primary", use_container_width=True):
            if api_key and len(api_key.strip()) > 0:
                st.session_state["gemini_api_key"] = api_key.strip()
                st.success("✅ API Key stored successfully in your current session!")
            else:
                st.error("Please enter a valid API key.")
        
        # Show current status
        if st.session_state.get("gemini_api_key"):
            st.info("📌 API Key is currently configured for this session.")

    with col2:
        render_card(
            title="Need an API Key?",
            body="""
            Get your free Gemini API key from Google AI Studio:
            <ol style="margin-top: 10px; padding-left: 20px;">
                <li style="margin-bottom: 8px;">Visit Google AI Studio</li>
                <li style="margin-bottom: 8px;">Sign in or create an account</li>
                <li style="margin-bottom: 8px;">Create a new API key</li>
                <li style="margin-bottom: 8px;">Copy and paste it here</li>
            </ol>
            """
        )
        
        st.markdown("""
        <a href="https://aistudio.google.com/app/apikey" target="_blank" style="text-decoration: none;">
            <button style="
                width: 100%;
                background: rgba(30, 41, 59, 0.5);
                color: #38bdf8;
                border: 1px solid rgba(56, 189, 248, 0.3);
                padding: 12px 20px;
                border-radius: 12px;
                font-size: 0.95rem;
                font-weight: 600;
                cursor: pointer;
                font-family: 'Outfit', sans-serif;
                transition: all 0.3s ease;
            ">
                🔗 Open Google AI Studio
            </button>
        </a>
        """, unsafe_allow_html=True)

    # Security Note
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    render_card(
        title="🔒 Security Information",
        body="""
        <b>Important:</b> Your API keys are stored <b>only in your current browser session</b> and are never saved to disk or transmitted to any third-party servers except when making direct API calls to the respective AI services. When you close this tab or refresh the page, your API key will be cleared.
        """
    )
