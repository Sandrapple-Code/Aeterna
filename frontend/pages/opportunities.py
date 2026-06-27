import streamlit as st
from frontend.components.cards import render_card


def render_opportunities_page() -> None:
    """
    Renders the Opportunities page
    """
    # Page header with home button
    col_home, col_title = st.columns([1, 5])
    with col_home:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_page = "Landing"
            st.rerun()
    with col_title:
        st.markdown('<div class="dashboard-title">🌍 Opportunities</div>', unsafe_allow_html=True)
        st.markdown('<div class="dashboard-subtitle">Personalized internships, jobs, and more</div>', unsafe_allow_html=True)
        
    # Check if analysis is generated
    if not st.session_state.get("analysis_generated"):
        st.info("Complete a Career Discovery analysis first to see personalized opportunities!")
        if st.button("🧭 Start Career Discovery", type="primary"):
            st.session_state.current_page = "Career Discovery"
            st.rerun()
        return
        
    # Get opportunities data
    result = st.session_state.analysis_result
    opportunities = result.get("opportunities", {}).get("opportunities", {})
    
    # Render each category
    categories = [
        ("💼 Jobs", opportunities.get("jobs", [])),
        ("🎓 Internships", opportunities.get("internships", [])),
        ("🚀 Hackathons", opportunities.get("hackathons", [])),
        ("🎯 Fellowships", opportunities.get("fellowships", [])),
        ("🏢 Recommended Companies", opportunities.get("recommended_companies", []))
    ]
    
    for category_title, items in categories:
        if not items:
            continue
            
        st.subheader(category_title)
        
        if category_title == "🏢 Recommended Companies":
            cols = st.columns(3)
            for i, company in enumerate(items):
                with cols[i % 3]:
                    render_card(
                        title=company,
                        body="Recommended for you"
                    )
        else:
            for item in items:
                body_parts = []
                for key, val in item.items():
                    if key not in ["title", "link"]:
                        body_parts.append(f"- {key.replace('_', ' ').title()}: {val}")
                render_card(
                    title=item.get("title", "Opportunity"),
                    body="\n".join(body_parts) if body_parts else "Click for more details"
                )
