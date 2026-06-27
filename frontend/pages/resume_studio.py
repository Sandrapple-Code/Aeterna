import streamlit as st
from frontend.components.cards import render_card

def render_resume_studio_page() -> None:
    """
    Renders the Aeterna Resume Studio.
    Provides resume file parsing inputs, job description matching, 
    and downloads for AI-tailored PDFs.
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
        st.markdown('<div class="dashboard-title">Resume Studio</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="dashboard-subtitle">Tailor your resume perfectly for your dream job</div>',
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

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📥 Upload & Match")
        
        # File uploader stub
        uploaded_file = st.file_uploader("Upload Current Resume (PDF)", type=["pdf"])
        
        # Job description input
        job_desc = st.text_area("Target Job Description", height=250, placeholder="Paste the job requirements here...")
        
        # Optimization Trigger Button
        optimize_clicked = st.button("🚀 Match & Optimize Resume", type="primary", use_container_width=True)
        
        if optimize_clicked:
            if not uploaded_file or not job_desc:
                st.error("Please upload a resume and provide a target job description.")
            else:
                with st.spinner("Optimizing your resume..."):
                    from services.llm_service import LLMService
                    from services.db_service import DBService
                    from agents.resume_optimizer import ResumeOptimizer
                    
                    llm_service = LLMService()
                    api_key = st.session_state.get("gemini_api_key")
                    if api_key and "dummy" not in api_key.lower() and "mock" not in api_key.lower():
                        from google import genai
                        llm_service.client = genai.Client(api_key=api_key)
                    db = DBService()
                    agent = ResumeOptimizer(llm_service, db)
                    from utils.pdf_extractor import extract_text_from_pdf
                    resume_text = extract_text_from_pdf(uploaded_file)
                    resume_res = agent.run({
                        "resume_text": resume_text,
                        "job_description": job_desc
                    })
                    
                    if "analysis_result" not in st.session_state:
                        st.session_state.analysis_result = {}
                    st.session_state.analysis_result["resume"] = resume_res
                    st.session_state.analysis_generated = True
                    st.rerun()

    with col2:
        st.subheader("🎯 Optimization Insights")

        # Check if there is an existing resume optimization result
        analysis_result = st.session_state.get("analysis_result")
        resume_res = analysis_result.get("resume") if analysis_result else None
        
        if resume_res:
            if not resume_res.get("success", False):
                st.warning(resume_res.get("error", "Generation failed."))
            else:
                if resume_res.get("is_mock"):
                    st.warning("⚠️ Running in Offline Mode: Gemini API rate limit or key restriction hit. Showing adaptive mock resume insights. Re-submit with a valid key for live parsing.")
                insights = resume_res.get("structured_insights", {})
                match_score = insights.get("match_score", 0)
                st.metric("🎯 Resume Match Score", f"{match_score}%" if isinstance(match_score, (int, float)) else str(match_score))
                
                st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
                st.write("**🔍 Skill Gaps Identified:**")
                for gap in insights.get("skill_gaps_identified", []):
                    st.markdown(f"- {gap}")
                    
                st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
                st.write("**💎 Optimized Bullets Suggested (STAR/XYZ):**")
                for bullet in insights.get("optimized_bullets_suggested", []):
                    st.markdown(f"- {bullet}")
                    
                if resume_res.get("raw_analysis"):
                    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
                    with st.expander("📄 View Full Narrative Analysis"):
                        st.write(resume_res.get("raw_analysis"))
        else:
            st.info("Provide your resume and a target job description, then click 'Match & Optimize' to initiate the CareerForge Engine.")
            
            # Illustrative cards
            render_card(
                title="⚡ AI-Powered Keyword Analysis",
                body="CareerForge automatically extracts key hard skills, soft skills, and experiences required by the employer and maps them to your resume."
            )
            render_card(
                title="💎 Professional Impact Formulas",
                body="Transform passive resume descriptions into powerful, metrics-driven bullets following Google's XYZ formula."
            )
