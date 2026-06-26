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
from frontend.pages.interview_prep import render_interview_prep_page
from frontend.pages.landing import render_landing_page

# 2. Centralized Logger & Settings Initialization
settings = get_settings()
configure_logger(log_level=settings.log_level)

# 3. Inject Premium Custom CSS
def inject_custom_css() -> None:
    """
    Reads custom.css and injects it into the Streamlit application body.
    """
    css_path = os.path.join("frontend", "styles", "custom.css")
    if os.path.exists(css_path):
        try:
            with open(css_path, "r", encoding="utf-8") as f:
                css_content = f.read()
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
            if active_page == "Dashboard":
                render_dashboard_page()
            elif active_page == "Resume Studio":
                render_resume_studio_page()
            elif active_page == "Interview Prep":
                render_interview_prep_page()
            else:
                logger.error(f"Unhandled page route: {active_page}")
                st.error(f"Page '{active_page}' not found.")
            
    except Exception as e:
        logger.exception("An unhandled exception occurred in the application main thread.")
        st.error("A critical system error occurred. Please check application logs for details.")

if __name__ == "__main__":
    main()
