import streamlit as st
from frontend.components.cards import render_card
from services.llm_service import LLMService
from services.db_service import DBService
from services.pdf_service import PDFService
from agents.resume_optimizer import ResumeOptimizer

def render_resume_studio_page() -> None:
    """
    Renders the Aeterna Resume Studio.
    Provides resume file parsing inputs, job description matching, 
    and downloads for AI-tailored PDFs.
    """
    # Header
    st.markdown('<div class="dashboard-title">Resume Studio</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="dashboard-subtitle">Tailor your resume perfectly for your dream job with the CareerForge Optimizer.</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📥 Upload & Match")
        
        # File uploader stub
        uploaded_file = st.file_uploader("Upload Current Resume (PDF)", type=["pdf"])
        
        # Job description input
        job_desc = st.text_area("Target Job Description", height=250, placeholder="Paste the job requirements here...")
        
        # Optimization Trigger Button
        optimize_clicked = st.button("🚀 Match & Optimize Resume", type="primary", use_container_width=True)

    with col2:
        st.subheader("🎯 Optimization Insights")

        # Mock / Placeholder State before optimization is clicked
        if not optimize_clicked:
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
        else:
            # When clicked, show loading state and stub outputs
            with st.spinner("CareerForge Engine analyzing skills and matching criteria..."):
                # Scaffold dependency injection
                llm = LLMService()
                db = DBService()
                pdf = PDFService()
                optimizer = ResumeOptimizer(llm, db)
                
                # Mock inputs for prompt processing
                mock_input = {
                    "resume_text": "Experienced Python Software Engineer with 5 years experience.",
                    "job_description": job_desc if job_desc else "Requires senior software architect with expert Python, LLM orchestration and Streamlit experience."
                }
                
                # Execute optimizer agent
                result = optimizer.run(mock_input)
                
            if result.get("success"):
                st.success("Analysis complete! Optimized resume generated.")
                
                # Display Match Score
                match_score = result["structured_insights"]["match_score"]
                st.metric("Tailored Job Fit Score", f"{match_score}%", delta="15% improvement")
                
                # Display Skill Gaps
                st.markdown("### ⚠️ Critical Skill Gaps Detected")
                for gap in result["structured_insights"]["skill_gaps_identified"]:
                    st.markdown(f"- **{gap}** (Missing in uploaded profile)")
                
                # Display Suggested Bullet Points
                st.markdown("### ✨ Suggested Tailored Bullet Points")
                for bullet in result["structured_insights"]["optimized_bullets_suggested"]:
                    st.info(bullet)
                    
                # Compile PDF Action
                st.markdown("### 📄 Export Production Resume")
                
                # Render content compile
                resume_content = f"""
                John Doe
                Senior Software Engineer
                
                ## Professional Summary
                Tailored profile targeting modern AI/ML Full-Stack engineering roles.
                
                ## Key Experience Bullet Points
                - {result["structured_insights"]["optimized_bullets_suggested"][0]}
                - {result["structured_insights"]["optimized_bullets_suggested"][1]}
                
                ## Skills Matrix
                Python, Streamlit, Pydantic, LLM Orchestration, Docker, Kubernetes, CI/CD, FastAPI, Kafka
                """
                
                try:
                    # Generate actual PDF via PDFService
                    pdf_path = pdf.generate_resume_pdf("John Doe", resume_content, "optimized_resume_john_doe.pdf")
                    
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            label="📥 Download Tailored Resume PDF",
                            data=f,
                            file_name="Optimized_Resume_John_Doe.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"Failed to generate download package: {e}")
            else:
                st.error(f"Optimization failed: {result.get('error')}")

    # TODO: Connect actual PyPDF2/pdf plumbing to extract text from uploaded_file
    # TODO: Connect actual structured LLM response mapping to save generated resume to DBService
