"""
frontend/pages/career_discovery.py
"""
import streamlit as st
from frontend.components.cards import render_card
from services.llm_service import LLMService
from services.db_service import DBService
from agents.career_discovery import CareerDiscoveryAgent
from agents.resume_optimizer import ResumeOptimizer
from agents.career_pathfinder import CareerPathfinder
from agents.opportunity_agent import OpportunityAgent


def _make_llm() -> LLMService:
    """Always returns an LLMService that picks up the current session API key."""
    llm = LLMService()
    api_key = st.session_state.get("gemini_api_key", "").strip()
    if api_key:
        from google import genai
        llm.client = genai.Client(api_key=api_key)
    return llm


class CareerForgeEngine:
    def __init__(self, llm: LLMService, db):
        self.llm = llm
        self.db  = db

    def run_pipeline(self, user_input: dict, resume_text: str | None = None) -> dict:
        """
        Full pipeline:  Discovery → Resume → Pathfinder → Opportunities
        user_input keys: education, current_year, interests, skills, work_style, goals
        """
        interests          = user_input.get("interests", "")
        skills             = user_input.get("skills", "")
        goals              = user_input.get("goals", "")

        # ── 1. Career Discovery ───────────────────────────────────────────────
        discovery_agent  = CareerDiscoveryAgent(self.llm, self.db)
        discovery_result = discovery_agent.run(user_input)

        if not discovery_result.get("success"):
            return {
                "discovery":     discovery_result,
                "planner":       {"success": False, "error": "Discovery failed.", "roadmap": None},
                "resume":        {"success": False, "error": "Discovery failed.", "structured_insights": None},
                "opportunities": {"success": False, "error": "Discovery failed.", "opportunities": None},
            }

        recommended_career = (
            discovery_result.get("career_matches", {}).get("recommended_career", "") or ""
        )

        # ── 2. Resume Optimisation (optional) ────────────────────────────────
        resume_result = None
        resume_gaps   = []
        if resume_text:
            resume_agent  = ResumeOptimizer(self.llm, self.db)
            resume_result = resume_agent.run({
                "resume_text":      resume_text,
                "job_description":  recommended_career or goals,
            })
            if resume_result.get("success"):
                resume_gaps = (
                    resume_result.get("structured_insights", {})
                    .get("skill_gaps_identified", [])
                )

        # ── 3. Career Pathfinder ──────────────────────────────────────────────
        planner_agent  = CareerPathfinder(self.llm, self.db)
        planner_result = planner_agent.run({
            "current_role":       user_input.get("education", "Student"),
            "target_destination": recommended_career,
            "skill_profile":      skills,
            "recommended_career": recommended_career,
            "resume_skill_gaps":  ", ".join(resume_gaps) if resume_gaps else "",
        })

        # ── 4. Opportunities ──────────────────────────────────────────────────
        opp_agent  = OpportunityAgent(self.llm, self.db)
        opp_result = opp_agent.run({
            # Core user profile – these drive personalisation
            "interests":          interests,
            "skills":             skills,
            "goals":              goals,
            "recommended_career": recommended_career,
            # Extra context from earlier agents
            "roadmap_summary":    planner_result.get("raw_analysis", "") if planner_result and planner_result.get("success") else "",
            "resume_summary":     resume_result.get("raw_analysis", "") if resume_result and resume_result.get("success") else "",
        })

        return {
            "discovery":     discovery_result,
            "planner":       planner_result,
            "resume":        resume_result,
            "opportunities": opp_result,
        }


# ── Page renderer ─────────────────────────────────────────────────────────────

def render_career_discovery_page() -> None:
    if "intake_step" not in st.session_state:
        st.session_state.intake_step = 1
    if "intake_data" not in st.session_state:
        st.session_state.intake_data = {}

    # ── Already have analysis ────────────────────────────────────────────────
    if st.session_state.get("analysis_generated"):
        st.markdown("### ✨ Career Analysis Active")
        st.info(
            "You already have a personalised career analysis. "
            "View results on the Dashboard, or regenerate below to update your profile."
        )
        data = st.session_state.get("intake_data", {})
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**Education:** {data.get('education','N/A')}")
            st.markdown(f"**Stage/Experience:** {data.get('current_year','N/A')}")
            st.markdown(f"**Work Style:** {data.get('work_style','N/A')}")
        with c2:
            st.markdown(f"**Interests:** {data.get('interests','N/A')}")
            st.markdown(f"**Skills:** {data.get('skills','N/A')}")
            st.markdown(f"**Goals:** {data.get('goals','N/A')}")
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        if st.button("🔄 Regenerate Career Analysis", type="primary", use_container_width=True):
            st.session_state.analysis_generated = False
            st.session_state.intake_step = 1
            st.rerun()
        return

    # ── Page header ──────────────────────────────────────────────────────────
    col_home, col_title = st.columns([1, 5])
    with col_home:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_page = "Landing"
            st.rerun()
    with col_title:
        st.markdown('<div class="dashboard-title">🧭 Career Discovery</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="dashboard-subtitle">Find your perfect career path with AI guidance</div>',
            unsafe_allow_html=True,
        )

    st.progress(st.session_state.intake_step / 3)
    st.caption(f"Step {st.session_state.intake_step} of 3")

    # ── Step 1 ────────────────────────────────────────────────────────────────
    if st.session_state.intake_step == 1:
        st.markdown("### Step 1 — Profile Basics")
        education = st.selectbox(
            "Education Level",
            ["High School", "Undergraduate", "Graduate", "Postgraduate", "Working Professional"],
            index=st.session_state.intake_data.get("education_idx", 0),
        )
        current_year = st.text_input(
            "Current Year / Experience Level",
            value=st.session_state.intake_data.get("current_year", ""),
            placeholder="e.g. '2nd Year Undergraduate' or '3 Years Work Experience'",
        )
        if st.button("Next →", type="primary", use_container_width=True):
            edu_opts = ["High School","Undergraduate","Graduate","Postgraduate","Working Professional"]
            st.session_state.intake_data.update({
                "education":      education,
                "current_year":   current_year,
                "education_idx":  edu_opts.index(education),
            })
            st.session_state.intake_step = 2
            st.rerun()

    # ── Step 2 ────────────────────────────────────────────────────────────────
    elif st.session_state.intake_step == 2:
        st.markdown("### Step 2 — Interests & Goals")
        st.caption(
            "💡 Be SPECIFIC — the AI uses exactly what you write here. "
            "'Cloud Computing, AWS, Kubernetes' gives far better results than just 'tech'."
        )
        interests = st.text_area(
            "Your Interests ✳️",
            value=st.session_state.intake_data.get("interests", ""),
            placeholder=(
                "Examples:\n"
                "• Cloud Computing, AWS, DevOps, Kubernetes, infrastructure automation\n"
                "• Robotics, ROS2, embedded systems, autonomous vehicles\n"
                "• Finance, algorithmic trading, risk modelling, fintech\n"
                "• Web development, React, Node.js, full-stack"
            ),
            height=130,
        )
        skills = st.text_area(
            "Your Current Skills",
            value=st.session_state.intake_data.get("skills", ""),
            placeholder="e.g. Python, SQL, basic Linux, some AWS experience, React basics",
            height=90,
        )
        work_style = st.selectbox(
            "Preferred Work Style",
            ["Independent", "Collaborative", "Fast-Paced", "Structured"],
            index=st.session_state.intake_data.get("work_style_idx", 0),
        )
        goals = st.text_area(
            "Your Career Goals",
            value=st.session_state.intake_data.get("goals", ""),
            placeholder="e.g. Become a Cloud Solutions Architect at a top company within 2 years",
            height=90,
        )
        col_back, col_next = st.columns(2)
        with col_back:
            if st.button("← Back", use_container_width=True):
                st.session_state.intake_step = 1
                st.rerun()
        with col_next:
            if st.button("Next →", type="primary", use_container_width=True):
                if not interests.strip() and not skills.strip():
                    st.error("Please fill in at least your interests or skills.")
                else:
                    ws_opts = ["Independent","Collaborative","Fast-Paced","Structured"]
                    st.session_state.intake_data.update({
                        "interests":       interests,
                        "skills":          skills,
                        "work_style":      work_style,
                        "work_style_idx":  ws_opts.index(work_style),
                        "goals":           goals,
                    })
                    st.session_state.intake_step = 3
                    st.rerun()

    # ── Step 3 ────────────────────────────────────────────────────────────────
    elif st.session_state.intake_step == 3:
        st.markdown("### Step 3 — Resume Upload (Optional)")
        st.caption("Skip if you don't have one — the full analysis still runs.")

        uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

        col_back, col_go = st.columns(2)
        with col_back:
            if st.button("← Back", use_container_width=True):
                st.session_state.intake_step = 2
                st.rerun()
        with col_go:
            if st.button("🚀 Generate My Career Analysis", type="primary", use_container_width=True):
                # Check API key before running
                if not st.session_state.get("gemini_api_key"):
                    st.error(
                        "⚠️ No Gemini API key found. "
                        "Please enter your key under ⚙️ Settings first."
                    )
                    st.stop()

                resume_text = None
                if uploaded_file:
                    from utils.pdf_extractor import extract_text_from_pdf
                    resume_text = extract_text_from_pdf(uploaded_file)

                # ── Run the pipeline (spinner wraps the WHOLE thing) ──────────
                with st.spinner(
                    "CareerForge Engine is working… "
                    "analysing your profile, building your roadmap, "
                    "and searching for opportunities. "
                    "This may take 30–90 seconds."
                ):
                    llm = _make_llm()
                    db  = DBService()
                    engine = CareerForgeEngine(llm, db)
                    result = engine.run_pipeline(st.session_state.intake_data, resume_text)

                # Auto-generate PDF
                try:
                    from services.pdf_service import PDFService
                    PDFService().compile_full_report(result, st.session_state.intake_data)
                except Exception as e:
                    st.warning(f"PDF report skipped: {e}")

                st.session_state.analysis_result    = result
                st.session_state.analysis_generated = True
                st.session_state.intake_step        = 1
                st.session_state.current_page       = "Dashboard"
                st.rerun()