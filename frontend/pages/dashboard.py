import streamlit as st
from frontend.components.cards import render_card, render_stat_card


def render_dashboard_page() -> None:
    """
    Renders the Aeterna Main Cockpit Dashboard.
    """
    # Initialize settings panel state
    if "show_settings" not in st.session_state:
        st.session_state.show_settings = False
        
    # Header with Home button
    col_home, col_title = st.columns([1, 5])
    with col_home:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_page = "Landing"
            st.rerun()
            
    with col_title:
        st.markdown('<div class="dashboard-title">Career Cockpit</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="dashboard-subtitle">Your personalized career hub</div>',
            unsafe_allow_html=True
        )
        
    # Settings button
    if st.button("⚙️ Settings", use_container_width=False):
        st.session_state.show_settings = not st.session_state.show_settings
        st.rerun()
        
    # Settings Expandable Panel
    if st.session_state.show_settings:
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        with st.expander("⚙️ Settings - Gemini API Configuration", expanded=True):
            col1, col2 = st.columns([2, 1])
            with col1:
                api_key = st.text_input(
                    "Enter your Gemini API Key",
                    type="password",
                    placeholder="Enter your Gemini API Key",
                    value=st.session_state.get("gemini_api_key", ""),
                    help="Your API key is stored only in your session and never saved permanently"
                )
                
                if st.button("Validate API Key", type="primary", use_container_width=True):
                    if api_key and len(api_key.strip()) > 0:
                        st.session_state["gemini_api_key"] = api_key.strip()
                        st.success("✅ API Key stored successfully in your current session!")
                        st.session_state.show_settings = False
                        st.rerun()
                    else:
                        st.error("Please enter a valid API key.")
            
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
            
            render_card(
                title="🔒 Security Information",
                body="""
                <b>Important:</b> Your API keys are stored <b>only in your current browser session</b>.
                """
            )

    # Check if analysis is generated
    analysis_generated = st.session_state.get("analysis_generated")
    result = st.session_state.get("analysis_result") if analysis_generated else None
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Career Readiness
    with col1:
        if analysis_generated and result:
            planner_res = result.get("planner", {})
            if not planner_res.get("success", False):
                st.warning(planner_res.get("error", "Generation failed."))
            else:
                cr_score = planner_res.get("roadmap", {}).get("career_readiness_score", "Not Generated")
                value = f"{cr_score}%" if isinstance(cr_score, (int, float)) else str(cr_score)
                render_stat_card(
                    label="📊 Career Readiness",
                    value=value
                )
        else:
            render_stat_card(
                label="📊 Career Readiness",
                value="Not Generated"
            )
            
    # Career Match
    with col2:
        if analysis_generated and result:
            discovery_res = result.get("discovery", {})
            if not discovery_res.get("success", False):
                st.warning(discovery_res.get("error", "Generation failed."))
            else:
                cm = discovery_res.get("career_matches", {}).get("recommended_career", "Not Generated")
                render_stat_card(
                    label="🎯 Career Match",
                    value=str(cm)
                )
        else:
            render_stat_card(
                label="🎯 Career Match",
                value="Not Generated"
            )
            
    # Roadmap (link to Career Planner)
    with col3:
        if analysis_generated and result:
            planner_res = result.get("planner", {})
            if not planner_res.get("success", False):
                st.warning(planner_res.get("error", "Generation failed."))
            else:
                phases = planner_res.get("roadmap", {}).get("phases", [])
                roadmap_title = phases[0].get("title", "Not Generated") if phases else "Not Generated"
                render_stat_card(
                    label="🗺️ Roadmap",
                    value=str(roadmap_title)
                )
        else:
            render_stat_card(
                label="🗺️ Roadmap",
                value="Not Generated"
            )
            
    # Resume Analysis
    with col4:
        if analysis_generated and result and result.get("resume"):
            resume_res = result.get("resume", {})
            if not resume_res.get("success", False):
                st.warning(resume_res.get("error", "Generation failed."))
            else:
                match_score = resume_res.get("structured_insights", {}).get("match_score", "No Resume Uploaded")
                value = f"{match_score}%" if isinstance(match_score, (int, float)) else str(match_score)
                render_stat_card(
                    label="📄 Resume Analysis",
                    value=value
                )
        else:
            render_stat_card(
                label="📄 Resume Analysis",
                value="No Resume Uploaded"
            )
            
    # Latest Opportunities
    with col5:
        if analysis_generated and result:
            opp_res = result.get("opportunities", {})
            if not opp_res.get("success", False):
                st.warning(opp_res.get("error", "Generation failed."))
            else:
                jobs = opp_res.get("opportunities", {}).get("jobs", [])
                render_stat_card(
                    label="🌍 Latest Opportunities",
                    value=f"{len(jobs)} New Matches"
                )
        else:
            render_stat_card(
                label="🌍 Latest Opportunities",
                value="Not Generated"
            )
        
    # Quick Actions
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    st.subheader("⚡ Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📄 Resume Studio", use_container_width=True):
            st.session_state.current_page = "Resume Studio"
            st.rerun()
    with col2:
        if st.button("🧭 Start Career Discovery", use_container_width=True):
            st.session_state.current_page = "Career Discovery"
            st.rerun()
    with col3:
        if st.button("🌍 Opportunities", use_container_width=True, disabled=not analysis_generated):
            st.session_state.current_page = "Opportunities"
            st.rerun()
    with col4:
        if st.button("📊 Reports", use_container_width=True, disabled=not analysis_generated):
            st.session_state.current_page = "Reports"
            st.rerun()
