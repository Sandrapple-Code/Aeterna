import os
import streamlit as st
from loguru import logger

# 1. Page Configurations (MUST be the first Streamlit command)
st.set_page_config(
    page_title="Aeterna — The Career Operating System",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

from config.settings import get_settings
from utils.logger import configure_logger
from frontend.components.sidebar import render_sidebar
from frontend.pages.dashboard import render_dashboard_page
from frontend.pages.resume_studio import render_resume_studio_page
from frontend.pages.career_discovery import render_career_discovery_page
from frontend.pages.landing import render_landing_page
from frontend.pages.career_planner import render_career_planner_page
from frontend.pages.opportunities import render_opportunities_page
from frontend.pages.reports import render_reports_page
from frontend.pages.settings import render_settings_page
from frontend.pages.chatbot import render_chatbot_page
from frontend.pages.login import render_login_page
from frontend.components.cards import render_card

# 2. Centralized Logger & Settings Initialization
settings = get_settings()
configure_logger(log_level=settings.log_level)

# 3. Inject Premium Custom CSS
def inject_custom_css() -> None:
    """
    Reads custom.css and injects it into the Streamlit application body, supporting dark/light themes.
    """
    css_path = os.path.join("frontend", "styles", "custom.css")
    if os.path.exists(css_path):
        try:
            with open(css_path, "r", encoding="utf-8") as f:
                css_content = f.read()
            
            # Inject gradient text utility class
            gradient_text_css = """
            .aeterna-gradient-text {
                background: linear-gradient(135deg, #a855f7 0%, #38bdf8 100%) !important;
                -webkit-background-clip: text !important;
                -webkit-text-fill-color: transparent !important;
                color: transparent !important;
                display: inline-block;
            }
            """
            css_content += gradient_text_css
            
            # Inject light mode override styles if selected
            if st.session_state.get("theme", "dark") == "light":
                light_css = """
                .stApp {
                    background: radial-gradient(circle at 10% 20%, #f8fafc 0%, #cbd5e1 90%) !important;
                    color: #0f172a !important;
                }
                .aeterna-card {
                    background: rgba(255, 255, 255, 0.8) !important;
                    border: 1px solid rgba(0, 0, 0, 0.08) !important;
                    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.05) !important;
                }
                .aeterna-card-header {
                    color: #0f172a !important;
                }
                .aeterna-card-body {
                    color: #334155 !important;
                }
                .dashboard-title {
                    background: linear-gradient(135deg, #0284c7 0%, #7c3aed 100%) !important;
                    -webkit-background-clip: text !important;
                    -webkit-text-fill-color: transparent !important;
                }
                .dashboard-subtitle {
                    color: #475569 !important;
                }
                /* Sidebar button overrides */
                .nav-button {
                    color: #475569 !important;
                }
                .nav-button:hover {
                    color: #0284c7 !important;
                    background: rgba(2, 132, 199, 0.08) !important;
                }
                """
                css_content += light_css
                
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
            logger.info("Custom premium stylesheet successfully injected.")
        except Exception as e:
            logger.error(f"Failed to inject custom CSS: {e}")
    else:
        logger.warning(f"CSS file not found at: {css_path}")

inject_custom_css()

def main() -> None:
    """
    Main application orchestrator.
    Renders custom navigation and routes to corresponding views.
    """
    logger.info("Main application loop execution started.")
    
    # Enforce authentication
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        
    if not st.session_state.logged_in:
        render_login_page()
        return
        
    try:
        # Initialize landing page as default
        if "current_page" not in st.session_state:
            st.session_state.current_page = "Landing"
        
        # Render Landing page if selected, otherwise render sidebar + other pages
        if st.session_state.current_page == "Landing":
            render_landing_page()
        else:
            # Render Sidebar and capture selected navigation page
            active_page = render_sidebar()
            logger.info(f"Active navigation route: {active_page}")
            
            # Route to respective page modules
            if active_page == "Career Discovery":
                render_career_discovery_page()
            elif active_page == "Dashboard":
                render_dashboard_page()
            elif active_page == "Resume Studio":
                render_resume_studio_page()
            elif active_page == "Career Planner":
                render_career_planner_page()
            elif active_page == "Opportunities":
                render_opportunities_page()
            elif active_page == "Chatbot":
                render_chatbot_page()
            elif active_page == "Reports":
                render_reports_page()
            elif active_page == "Settings":
                render_settings_page()
            else:
                logger.error(f"Unhandled page route: {active_page}")
                st.error(f"Page '{active_page}' not found.")
            
    except Exception as e:
        logger.exception("An unhandled exception occurred in the application main thread.")
        st.error("A critical system error occurred. Please check application logs for details.")

if __name__ == "__main__":
    main()
