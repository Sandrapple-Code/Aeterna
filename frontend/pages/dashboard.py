import streamlit as st
from frontend.components.cards import render_card, render_stat_card

def render_dashboard_page() -> None:
    """
    Renders the Aeterna Main Cockpit Dashboard.
    Provides high-level metrics, active applications tracker, and quick launch actions.
    """
    # Header
    st.markdown('<div class="dashboard-title">Career Cockpit</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="dashboard-subtitle">Welcome back, John. Here is the real-time health of your career search.</div>',
        unsafe_allow_html=True
    )

    # Stat Cards Row
    col1, col2, col3 = st.columns(3)
    with col1:
        render_stat_card("Resume Match Score", "78%", "4.5% this week")
    with col2:
        render_stat_card("Mock Interviews", "12 Rounds", "3 completed")
    with col3:
        render_stat_card("Applications Tracked", "8 Active", "2 new")

    # Main Content Columns
    left_col, right_col = st.columns([2, 1])

    with left_col:
        st.subheader("🎯 Career Transition Progress")
        
        # Display elegant progress stubs
        render_card(
            title="🎯 Goal: Senior Full-Stack Engineer (AI/ML Integration)",
            body="""
            Your current trajectory shows strong progress in backend API architecture and frontend design.
            The primary skill gap remaining is <b>Large Language Model Orchestration</b>.
            """,
            badge="In Progress"
        )

        render_card(
            title="💼 Active Job Application: Tech Corp (Senior Engineer)",
            body="""
            <b>Stage:</b> Technical Screen Preparation<br>
            <b>Next Action:</b> Run mock behavioral and technical interview coaching loops.
            """,
            badge="Interview Scheduled"
        )

    with right_col:
        st.subheader("⚡ Quick Actions")
        
        st.markdown(
            """
            <div style="background: rgba(30, 41, 59, 0.2); border: 1px solid rgba(255, 255, 255, 0.05); 
                        border-radius: 12px; padding: 15px; margin-bottom: 20px;">
                <p style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 12px;">
                    Accelerate your workflow with CareerForge Engine tools:
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Trigger navigations by updating session state
        if st.button("📝 Optimize a Resume", use_container_width=True):
            st.session_state.current_page = "Resume Studio"
            st.rerun()
            
        if st.button("🎙️ Launch Mock Interview", use_container_width=True):
            st.session_state.current_page = "Interview Prep"
            st.rerun()

        # TODO: Add integrations to load dynamic statistics from DBService
        # TODO: Add dynamic notification system for upcoming mock interview reminders
