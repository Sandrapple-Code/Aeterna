import streamlit as st
from frontend.components.cards import render_card

def render_sidebar() -> str:
    """
    Renders a premium, customized navigation sidebar.
    Manages session state for page routing and returns the active page identifier.
    """
    # Initialize settings panel state
    if "show_settings" not in st.session_state:
        st.session_state.show_settings = False
        
    st.sidebar.markdown(
        """
        <div style="text-align: center; padding: 10px 0 20px 0;">
            <h1 style="font-family: 'Outfit', sans-serif; font-size: 2rem; font-weight: 800; 
                       background: linear-gradient(135deg, #38bdf8 0%, #a855f7 100%);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                       margin-bottom: 0px;">
                Aeterna
            </h1>
            <p style="color: #64748b; font-size: 0.8rem; letter-spacing: 0.05em; text-transform: uppercase; margin-top: 2px;">
                Career Operating System
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Home button
    if st.sidebar.button("🏠 Home", use_container_width=True, type="secondary"):
        st.session_state.current_page = "Landing"
        st.rerun()

    # Initialize navigation state
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Dashboard"

    # Navigation options
    pages = {
        "Dashboard": "📊 Dashboard",
        "Career Discovery": "🧭 Career Discovery",
        "Resume Studio": "📝 Resume Studio",
        "Career Planner": "📚 Career Planner",
        "Opportunities": "🌍 Opportunities",
        "Chatbot": "💬 Chatbot",
        "Reports": "📄 Reports",
        "Settings": "⚙️ Settings"
    }

    st.sidebar.markdown(
        """
        <div style="color: #64748b; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; 
                    letter-spacing: 0.05em; margin-bottom: 10px; padding-left: 10px; margin-top: 15px;">
            Core Modules
        </div>
        """,
        unsafe_allow_html=True
    )

    # Render custom buttons that manage session state
    for page_id, page_label in pages.items():
        is_active = st.session_state.current_page == page_id
        
        button_type = "primary" if is_active else "secondary"
        if st.sidebar.button(page_label, key=f"nav_{page_id}", use_container_width=True, type=button_type):
            st.session_state.current_page = page_id
            st.rerun()

    # Add Divider
    st.sidebar.markdown("<hr style='border-color: rgba(255, 255, 255, 0.08); margin: 20px 0;'>", unsafe_allow_html=True)

    # User Profile Widget at the bottom
    st.sidebar.markdown(
        """
        <div style="background: rgba(30, 41, 59, 0.3); border: 1px solid rgba(255, 255, 255, 0.05); 
                    border-radius: 12px; padding: 12px; display: flex; align-items: center; gap: 10px; margin-top: auto;">
            <div style="width: 36px; height: 36px; border-radius: 50%; 
                        background: linear-gradient(135deg, #38bdf8 0%, #a855f7 100%); 
                        display: flex; align-items: center; justify-content: center; 
                        font-weight: 700; color: white; font-family: 'Outfit', sans-serif;">
                JD
            </div>
            <div>
                <div style="font-size: 0.85rem; font-weight: 600; color: #f8fafc; line-height: 1.2;">John Doe</div>
                <div style="font-size: 0.7rem; color: #64748b; margin-top: 1px;">Premium Member</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    return st.session_state.current_page
