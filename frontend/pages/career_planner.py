import streamlit as st
from frontend.components.cards import render_card


def render_career_planner_page() -> None:
    """
    Renders the Career Planner page
    """
    # Page header with home button
    col_home, col_title = st.columns([1, 5])
    with col_home:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_page = "Landing"
            st.rerun()
    with col_title:
        st.markdown('<div class="dashboard-title">📚 Career Planner</div>', unsafe_allow_html=True)
        st.markdown('<div class="dashboard-subtitle">Your personalized career roadmap</div>', unsafe_allow_html=True)
        
    # Check if analysis is generated
    if not st.session_state.get("analysis_generated"):
        st.info("Complete a Career Discovery analysis first to see your personalized roadmap!")
        if st.button("🧭 Start Career Discovery", type="primary"):
            st.session_state.current_page = "Career Discovery"
            st.rerun()
        return
        
    # Get result
    result = st.session_state.analysis_result
    roadmap = result.get("planner", {}).get("roadmap", {})
    
    # Render estimated timeline
    st.subheader("⏱️ Estimated Timeline")
    render_card(
        title=roadmap.get("estimated_timeline", "12-18 Months"),
        body="Full career transition plan"
    )
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.subheader("📋 Roadmap Phases")
    
    # Render each phase
    phases = roadmap.get("phases", [])
    for phase in phases:
        render_card(
            title=phase.get("title", "Phase"),
            body="\n".join([f"- {obj}" for obj in phase.get("objectives", [])]),
            badge=phase.get("duration", "Duration TBD")
        )
        
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # Render Career Readiness Score
    if "career_readiness_score" in roadmap:
        st.metric(
            "🎯 Career Readiness Score",
            f"{roadmap['career_readiness_score']}" if isinstance(roadmap['career_readiness_score'], str) else f"{roadmap['career_readiness_score']}%"
        )
    else:
        render_card(
            title="Career Readiness Score",
            body="Coming Soon"
        )
