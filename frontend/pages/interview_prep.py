import streamlit as st
from services.llm_service import LLMService
from services.db_service import DBService
from agents.interview_coach import InterviewCoach

def render_interview_prep_page() -> None:
    """
    Renders the Aeterna Mock Interview Prep Console.
    Simulates a dynamic conversational hiring panel and provides detailed performance rubrics.
    """
    # Header
    st.markdown('<div class="dashboard-title">Interview Coach</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="dashboard-subtitle">Engage in highly realistic interactive mock interviews designed by the CareerForge Coach.</div>',
        unsafe_allow_html=True
    )

    # Initialize Interview Session States
    if "interview_active" not in st.session_state:
        st.session_state.interview_active = False
    if "transcript" not in st.session_state:
        st.session_state.transcript = []
    if "current_question" not in st.session_state:
        st.session_state.current_question = ""

    # Scaffolding services
    llm = LLMService()
    db = DBService()
    coach = InterviewCoach(llm, db)

    left_col, right_col = st.columns([1, 2])

    with left_col:
        st.subheader("⚙️ Panel Settings")
        
        target_role = st.text_input("Target Job Title", value="Senior Full-Stack Engineer")
        round_type = st.selectbox(
            "Interview Category", 
            ["Behavioral (STAR framework)", "System Design Architecture", "Coding & Core Algorithms"]
        )
        job_desc = st.text_area("Job Description / Role Requirements", height=150, placeholder="Paste job context...")

        if not st.session_state.interview_active:
            if st.button("🎙️ Start Interview Session", type="primary", use_container_width=True):
                st.session_state.interview_active = True
                st.session_state.transcript = []
                
                # Generate initial question
                with st.spinner("Hiring Manager drafting first question..."):
                    initial_question = coach.generate_question(target_role, job_desc, [])
                    st.session_state.current_question = initial_question
                    st.session_state.transcript.append({
                        "role": "Interviewer",
                        "content": initial_question
                    })
                st.rerun()
        else:
            if st.button("🛑 Complete & Grade Interview", type="secondary", use_container_width=True):
                st.session_state.interview_active = False
                st.session_state.show_scorecard = True
                st.rerun()

    with right_col:
        st.subheader("💬 Chat Console")

        if st.session_state.interview_active:
            # Render chat turns
            for turn in st.session_state.transcript:
                role = turn["role"]
                content = turn["content"]
                if role == "Interviewer":
                    st.chat_message("assistant").markdown(f"**Interviewer:** {content}")
                else:
                    st.chat_message("user").markdown(f"**You:** {content}")

            # Answer input form
            with st.form("chat_input_form", clear_on_submit=True):
                user_answer = st.text_area("Type your response here:", height=100)
                submit_answer = st.form_submit_button("Submit Response")

            if submit_answer and user_answer.strip():
                # Record user response
                st.session_state.transcript.append({
                    "role": "Candidate",
                    "content": user_answer.strip()
                })
                
                # Generate next question based on transcript
                with st.spinner("Interviewer is processing response..."):
                    next_question = coach.generate_question(target_role, job_desc, st.session_state.transcript)
                    st.session_state.current_question = next_question
                    st.session_state.transcript.append({
                        "role": "Interviewer",
                        "content": next_question
                    })
                st.rerun()

        elif getattr(st.session_state, "show_scorecard", False):
            st.success("🎉 Interview Session Finished! Constructive Scorecard Generated.")
            
            with st.spinner("Analyzing communication patterns and technical accuracy..."):
                # Run interview coach evaluation
                mock_eval_input = {
                    "target_role": target_role,
                    "job_description": job_desc,
                    "candidate_background": "Senior Dev",
                    "transcript": st.session_state.transcript
                }
                evaluation = coach.run(mock_eval_input)
                
            if evaluation.get("success"):
                scorecard = evaluation["scorecard"]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Overall Score", f"{scorecard['overall_score']}%")
                with col2:
                    st.metric("Communication", f"{scorecard['communication_score']}%")
                with col3:
                    st.metric("Technical Depth", f"{scorecard['technical_score']}%")

                st.markdown("### 📝 Constructive Coaching Feedback")
                st.write(evaluation["raw_feedback"])

                st.markdown("### 👍 Highlighted Strengths")
                for strg in scorecard["key_strengths"]:
                    st.markdown(f"- **{strg}**")

                st.markdown("### 📈 Areas for Improvement")
                for area in scorecard["improvement_areas"]:
                    st.markdown(f"- **{area}**")

                # Save session via DBService stub
                db.save_interview_session("mock_session_id", st.session_state.transcript)
            else:
                st.error("Could not run performance evaluation.")

            if st.button("🔄 Start New Practice Session"):
                st.session_state.show_scorecard = False
                st.rerun()
        else:
            st.info("Set up your interview category on the left panel and click 'Start Interview Session' to begin the mock simulation.")

    # TODO: Add speech-to-text / audio recording stubs for voice-based interviews
    # TODO: Integrate time tracking to analyze pacing and average response length
