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

    # Add a live refresh button
    col_ref, col_space = st.columns([2, 3])
    with col_ref:
        if st.button("🔄 Refresh & Search (Live Web Grounding)", use_container_width=True):
            with st.spinner("Searching the web for the latest opportunities..."):
                from services.llm_service import LLMService
                from services.db_service import DBService
                from agents.opportunity_agent import OpportunityAgent
                
                llm_svc = LLMService()
                api_key = st.session_state.get("gemini_api_key")
                if api_key and "dummy" not in api_key.lower() and "mock" not in api_key.lower():
                    from google import genai
                    llm_svc.client = genai.Client(api_key=api_key)
                db = DBService()
                opp_agent = OpportunityAgent(llm_svc, db)
                
                result = st.session_state.analysis_result
                planner_res = result.get("planner", {})
                resume_res = result.get("resume", {})
                
                opp_result = opp_agent.run({
                    "roadmap_summary": planner_res.get("raw_analysis", "") if planner_res and planner_res.get("success") else "",
                    "resume_summary": resume_res.get("raw_analysis", "") if resume_res and resume_res.get("success") else ""
                })
                
                st.session_state.analysis_result["opportunities"] = opp_result
                st.toast("Opportunities successfully updated via live web search!", icon="✨")
                st.rerun()
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        
    # Get opportunities data
    result = st.session_state.analysis_result
    opp_res = result.get("opportunities", {})
    if not opp_res.get("success", False):
        st.warning(opp_res.get("error", "Generation failed."))
        return

    opportunities = opp_res.get("opportunities", {})
    
    # if opp_res.get("is_mock"):
    #     st.warning("⚠️ Running in Offline Mode: Gemini API rate limit or key restriction hit. Showing adaptive mock opportunities. Click the 'Refresh & Search' button above to retry live web scouting.")
    
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
                title = item if isinstance(item, str) else item.get("title", "Opportunity")
                if isinstance(item, str):
                    body = "Click the button below to get AI insights and application guidelines."
                else:
                    body_parts = []
                    for key, val in item.items():
                        if key not in ["title", "link"]:
                            body_parts.append(f"- {key.replace('_', ' ').title()}: {val}")
                    body = "\n".join(body_parts) if body_parts else "Click the button below to get AI insights and application guidelines."
                
                render_card(
                    title=title,
                    body=body
                )
                if st.button(f"🔍 Click for more details: {title}", key=f"details_{title.replace(' ', '_')}", use_container_width=True):
                    st.session_state.chatbot_query = f"Can you give me more details, tips, and step-by-step guidance on how to pursue this opportunity: '{title}'? Where should I look for it and what qualifications are usually required?"
                    st.session_state.current_page = "Chatbot"
                    st.rerun()
