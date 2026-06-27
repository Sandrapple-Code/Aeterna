import streamlit as st
from frontend.components.cards import render_card
from services.llm_service import LLMService










from services.db_service import DBService
from agents.career_discovery import CareerDiscoveryAgent
from agents.resume_optimizer import ResumeOptimizer
from agents.career_pathfinder import CareerPathfinder
from agents.opportunity_agent import OpportunityAgent


class MockCareerForgeEngine:
    def __init__(self, llm, db):
        self.llm = llm
        self.db = db
        
    def run_pipeline(self, user_input, resume_text=None):
        # Run all agents and return structured pipeline result
        discovery_agent = CareerDiscoveryAgent(self.llm, self.db)
        discovery_result = discovery_agent.run(user_input)
        
        if not discovery_result.get("success", False):
            return {
                "discovery": discovery_result,
                "planner": {
                    "success": False,
                    "error": "Upstream Career Discovery agent failed. Cannot generate roadmap.",
                    "roadmap": None
                },
                "resume": {
                    "success": False,
                    "error": "Upstream Career Discovery agent failed. Cannot run resume optimization.",
                    "structured_insights": None
                } if resume_text else None,
                "opportunities": {
                    "success": False,
                    "error": "Upstream Career Discovery agent failed. Cannot recommend opportunities.",
                    "opportunities": None
                }
            }

        recommended_career = discovery_result.get("career_matches", {}).get("recommended_career", "Unknown")

        resume_result = None
        resume_gaps = []
        if resume_text:
            resume_agent = ResumeOptimizer(self.llm, self.db)
            resume_result = resume_agent.run({
                "resume_text": resume_text,
                "job_description": recommended_career
            })
            if resume_result.get("success"):
                resume_gaps = resume_result.get("structured_insights", {}).get("skill_gaps_identified", [])
        
        planner_agent = CareerPathfinder(self.llm, self.db)
        planner_result = planner_agent.run({
            "current_role": user_input.get("education", "Student"),
            "target_destination": recommended_career,
            "skill_profile": user_input.get("skills", ""),
            "recommended_career": recommended_career,
            "resume_skill_gaps": ", ".join(resume_gaps) if resume_gaps else ""
        })

        opportunity_agent = OpportunityAgent(self.llm, self.db)
        opportunity_result = opportunity_agent.run({
            "roadmap_summary": planner_result.get("raw_analysis", "") if planner_result and planner_result.get("success") else "",
            "resume_summary": resume_result.get("raw_analysis", "") if resume_result and resume_result.get("success") else ""
        })
        
        return {
            "discovery": discovery_result,
            "planner": planner_result,
            "resume": resume_result,
            "opportunities": opportunity_result
        }


def render_career_discovery_page() -> None:
    """
    Renders the Career Discovery page with 3-step intake wizard
    """
    # Initialize session state
    if "intake_step" not in st.session_state:
        st.session_state.intake_step = 1
    if "intake_data" not in st.session_state:
        st.session_state.intake_data = {}

    # Option to see existing progress & regenerate analysis
    if st.session_state.get("analysis_generated"):
        st.markdown("### ✨ Career Analysis Active")
        st.info("You have already generated a personalized Career Analysis. You can view your results on the Dashboard or download your generated reports. If you wish to recalculate your path, you can regenerate it below.")
        
        data = st.session_state.get("intake_data", {})
        st.markdown("#### 📋 Current Profile Details")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Education Level:** {data.get('education', 'N/A')}")
            st.markdown(f"**Current Stage/Experience:** {data.get('current_year', 'N/A')}")
            st.markdown(f"**Preferred Work Style:** {data.get('work_style', 'N/A')}")
        with col2:
            st.markdown(f"**Interests:** {data.get('interests', 'N/A')}")
            st.markdown(f"**Skills:** {data.get('skills', 'N/A')}")
            st.markdown(f"**Career Goals:** {data.get('goals', 'N/A')}")
            
        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
        if st.button("🔄 Regenerate My Career Analysis", type="primary", use_container_width=True):
            st.session_state.analysis_generated = False
            st.session_state.intake_step = 1
            st.rerun()
        return
        
    # Page header with home button
    col_home, col_title = st.columns([1, 5])
    with col_home:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_page = "Landing"
            st.rerun()
    with col_title:
        st.markdown('<div class="dashboard-title">🧭 Career Discovery</div>', unsafe_allow_html=True)
        st.markdown('<div class="dashboard-subtitle">Find your perfect career path with AI guidance</div>', unsafe_allow_html=True)
        
    # Progress indicator
    progress_val = st.session_state.intake_step / 3
    st.progress(progress_val)
    st.caption(f"Step {st.session_state.intake_step} of 3")
    
    # Step 1: Profile Basics
    if st.session_state.intake_step == 1:
        st.markdown("### Profile Basics")
        
        education = st.selectbox(
            "Education Level",
            ["High School", "Undergraduate", "Graduate", "Postgraduate", "Working Professional"],
            index=st.session_state.intake_data.get("education_idx", 0)
        )
        current_year = st.text_input(
            "Current Year / Experience",
            value=st.session_state.intake_data.get("current_year", ""),
            placeholder="e.g., 'Junior' or '3 Years'"
        )
        
        if st.button("Next →", type="primary", use_container_width=True):
            st.session_state.intake_data["education"] = education
            st.session_state.intake_data["current_year"] = current_year
            st.session_state.intake_data["education_idx"] = ["High School", "Undergraduate", "Graduate", "Postgraduate", "Working Professional"].index(education)
            st.session_state.intake_step = 2
            st.rerun()
            
    # Step 2: Interests & Goals
    elif st.session_state.intake_step == 2:
        st.markdown("### Interests & Goals")
        
        interests = st.text_area(
            "Your Interests",
            value=st.session_state.intake_data.get("interests", ""),
            placeholder="What are you passionate about? (e.g., Cloud Computing, AI, Design)"
        )
        skills = st.text_area(
            "Your Skills",
            value=st.session_state.intake_data.get("skills", ""),
            placeholder="What skills do you have? (e.g., Python, React, Project Management)"
        )
        work_style = st.selectbox(
            "Preferred Work Style",
            ["Independent", "Collaborative", "Fast-Paced", "Structured"],
            index=st.session_state.intake_data.get("work_style_idx", 0)
        )
        goals = st.text_area(
            "Your Goals",
            value=st.session_state.intake_data.get("goals", ""),
            placeholder="What do you want to achieve in your career?"
        )
        
        col_back, col_next = st.columns([1, 1])
        with col_back:
            if st.button("← Back", use_container_width=True):
                st.session_state.intake_step = 1
                st.rerun()
        with col_next:
            if st.button("Next →", type="primary", use_container_width=True):
                st.session_state.intake_data["interests"] = interests
                st.session_state.intake_data["skills"] = skills
                st.session_state.intake_data["work_style"] = work_style
                st.session_state.intake_data["work_style_idx"] = ["Independent", "Collaborative", "Fast-Paced", "Structured"].index(work_style)
                st.session_state.intake_data["goals"] = goals
                st.session_state.intake_step = 3
                st.rerun()
                
    # Step 3: Resume (Optional)
    elif st.session_state.intake_step == 3:
        st.markdown("### Resume (Optional)")
        st.caption("Skip this if you don't have a resume yet — we'll still generate your full analysis.")
        
        uploaded_file = st.file_uploader(
            "Upload Resume (PDF)",
            type=["pdf"],
            help="Upload your resume for personalized analysis"
        )
        
        col_back, col_submit = st.columns([1, 1])
        with col_back:
            if st.button("← Back", use_container_width=True):
                st.session_state.intake_step = 2
                st.rerun()
        with col_submit:
            if st.button("🚀 Generate My Career Analysis", type="primary", use_container_width=True):
                resume_text = None
                if uploaded_file:
                    from utils.pdf_extractor import extract_text_from_pdf
                    resume_text = extract_text_from_pdf(uploaded_file)
                
                with st.spinner("CareerForge Engine is analyzing your profile and generating your personalized career path..."):
                    llm_service = LLMService()
                api_key = st.session_state.get("gemini_api_key")
                if api_key and "dummy" not in api_key.lower() and "mock" not in api_key.lower():
                    from google import genai
                    llm_service.client = genai.Client(api_key=api_key)
                db = DBService()
                engine = MockCareerForgeEngine(llm_service, db)
                result = engine.run_pipeline(st.session_state.intake_data, resume_text)
                
                # Automatically generate PDF report
                from services.pdf_service import PDFService
                pdf_svc = PDFService()
                pdf_svc.compile_full_report(result, st.session_state.intake_data)
                    
                st.session_state.analysis_result = result
                st.session_state.analysis_generated = True
                st.session_state.intake_step = 1
                st.session_state.current_page = "Dashboard"
                st.rerun()
