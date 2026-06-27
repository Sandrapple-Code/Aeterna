import streamlit as st
from config.settings import get_settings
from frontend.components.cards import render_card


def render_settings_page() -> None:
    """
    Renders the Settings page
    """
    # Page header with home button
    col_home, col_title = st.columns([1, 5])
    with col_home:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_page = "Landing"
            st.rerun()
    with col_title:
        st.markdown('<div class="dashboard-title">⚙️ Settings</div>', unsafe_allow_html=True)
        st.markdown('<div class="dashboard-subtitle">Configure your Aeterna settings</div>', unsafe_allow_html=True)
        
    # Get settings
    settings = get_settings()
    
    # Settings section
    st.subheader("🔧 Application Settings")
    
    # App Environment
    render_card(
        title="Environment",
        body=f"Current: {settings.app_env}"
    )
    
    # Log Level
    render_card(
        title="Log Level",
        body=f"Current: {settings.log_level}"
    )
    
    # Gemini API Key status
    has_key = st.session_state.get("gemini_api_key") is not None and len(st.session_state.get("gemini_api_key", "").strip()) > 0
    key_status = "✅ Configured" if has_key else "⚠️ Not Set"
    render_card(
        title="Gemini API Key",
        body=key_status
    )
    
    # Database URL
    render_card(
        title="Database URL",
        body=settings.database_url
    )
    
    # Theme selector (disabled placeholder)
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.subheader("🎨 Theme")
    st.selectbox(
        "Theme (Coming Soon)",
        ["Dark", "Light"],
        index=0,
        disabled=True,
        help="Theme customization will be available in a future update"
    )
