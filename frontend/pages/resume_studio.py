"""
frontend/pages/resume_studio.py
"""
import streamlit as st
from frontend.components.cards import render_card


def render_resume_studio_page() -> None:
    if "show_settings" not in st.session_state:
        st.session_state.show_settings = False

    col_home, col_title = st.columns([1, 5])
    with col_home:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_page = "Landing"
            st.rerun()
    with col_title:
        st.markdown('<div class="dashboard-title">📝 Resume Studio</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="dashboard-subtitle">Tailor your resume perfectly for your dream job</div>',
            unsafe_allow_html=True,
        )

    if st.button("⚙️ Settings", use_container_width=False):
        st.session_state.show_settings = not st.session_state.show_settings
        st.rerun()

    if st.session_state.show_settings:
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        with st.expander("⚙️ Gemini API Configuration", expanded=True):
            c1, c2 = st.columns([2, 1])
            with c1:
                api_key = st.text_input(
                    "Gemini API Key",
                    type="password",
                    value=st.session_state.get("gemini_api_key", ""),
                    placeholder="Paste your Gemini API key here",
                )
                if st.button("Save Key", type="primary", use_container_width=True):
                    if api_key.strip():
                        st.session_state["gemini_api_key"] = api_key.strip()
                        st.success("✅ Key saved!")
                        st.session_state.show_settings = False
                        st.rerun()
                    else:
                        st.error("Key cannot be empty.")
            with c2:
                render_card(
                    title="Get a free key",
                    body='Visit <a href="https://aistudio.google.com/app/apikey" target="_blank">Google AI Studio</a> → Get API Key',
                )

    # ── API key warning ───────────────────────────────────────────────────────
    if not st.session_state.get("gemini_api_key"):
        st.warning(
            "⚠️ No Gemini API key set — results will be mock data. "
            "Click ⚙️ Settings above to add your key."
        )

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📥 Upload & Match")
        uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
        job_desc = st.text_area(
            "Target Job Description",
            height=250,
            placeholder="Paste the full job description here…",
        )
        if st.button("🚀 Match & Optimize Resume", type="primary", use_container_width=True):
            if not uploaded_file or not job_desc.strip():
                st.error("Please upload a resume AND paste a job description.")
            else:
                with st.spinner("CareerForge is analysing your resume against the job description…"):
                    from services.llm_service import LLMService
                    from services.db_service import DBService
                    from agents.resume_optimizer import ResumeOptimizer
                    from utils.pdf_extractor import extract_text_from_pdf

                    resume_text = extract_text_from_pdf(uploaded_file)
                    agent = ResumeOptimizer(LLMService(), DBService())
                    result = agent.run({
                        "resume_text":     resume_text,
                        "job_description": job_desc,
                    })

                if "analysis_result" not in st.session_state:
                    st.session_state.analysis_result = {}
                st.session_state.analysis_result["resume"] = result
                st.session_state.analysis_generated = True
                st.rerun()

    with col2:
        st.subheader("🎯 Optimization Insights")
        analysis = st.session_state.get("analysis_result") or {}
        resume_res = analysis.get("resume")

        if resume_res:
            if not resume_res.get("success"):
                st.warning(resume_res.get("error", "Analysis failed."))
            else:
                if resume_res.get("is_mock"):
                    st.warning(
                        "⚠️ Offline Mode: Gemini API not reachable — showing mock insights. "
                        "Add your key in ⚙️ Settings and re-submit for live analysis."
                    )
                insights     = resume_res.get("structured_insights", {})
                match_score  = insights.get("match_score", 0)
                st.metric("🎯 Resume Match Score", f"{match_score}%")

                st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
                st.write("**🔍 Skill Gaps Identified:**")
                for gap in insights.get("skill_gaps_identified", []):
                    st.markdown(f"- {gap}")

                st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
                st.write("**💎 Optimized Bullets (STAR/XYZ):**")
                for bullet in insights.get("optimized_bullets_suggested", []):
                    st.markdown(f"- {bullet}")

                if resume_res.get("raw_analysis"):
                    st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
                    with st.expander("📄 Full Narrative Analysis"):
                        st.write(resume_res["raw_analysis"])
        else:
            st.info(
                "Upload your resume and paste a job description, "
                "then click 'Match & Optimize'."
            )
            render_card(
                title="⚡ ATS Keyword Analysis",
                body="CareerForge extracts every required skill from the job description and maps it to your resume.",
            )
            render_card(
                title="💎 XYZ Impact Bullets",
                body="Transforms passive resume lines into metrics-driven bullets using Google's XYZ formula.",
            )