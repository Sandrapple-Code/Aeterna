"""
frontend/pages/chatbot.py
"""
import streamlit as st
from google import genai
from services.llm_service import LLMService
from services.db_service import DBService
from agents.chatbot_agent import ChatbotAgent


def _make_agent() -> ChatbotAgent:
    """
    Creates ChatbotAgent with a correctly initialised LLMService.
    Explicitly injects the session API key into the client — same pattern
    used by resume_studio and career_discovery which work correctly.
    """
    llm = LLMService()
    api_key = st.session_state.get("gemini_api_key", "").strip()
    if api_key:
        llm.client = genai.Client(api_key=api_key)
    return ChatbotAgent(llm, DBService())


def _user_context() -> dict:
    return {
        "intake_data": st.session_state.get("intake_data", {}),
        "analysis_result": (
            st.session_state.get("analysis_result")
            if st.session_state.get("analysis_generated")
            else {}
        ),
    }


def render_chatbot_page() -> None:
    if "chatbot_history" not in st.session_state:
        st.session_state.chatbot_history = []
    if "current_chat_session_id" not in st.session_state:
        import uuid
        st.session_state.current_chat_session_id = str(uuid.uuid4())

    db_service = DBService()

    # ── Header ────────────────────────────────────────────────────────────────
    col_home, col_title, col_act1, col_act2 = st.columns([1, 4, 1, 1])
    with col_home:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_page = "Landing"
            st.rerun()
    with col_title:
        st.markdown('<div class="dashboard-title">💬 AI Career Coach</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="dashboard-subtitle">Ask me anything — I know your full profile</div>',
            unsafe_allow_html=True,
        )
    with col_act1:
        if st.button("💾 Save Chat", use_container_width=True, type="secondary"):
            db_service.save_chat_session(
                st.session_state.current_chat_session_id,
                st.session_state.chatbot_history
            )
            st.success("Chat saved successfully!")
            st.rerun()
    with col_act2:
        if st.button("📜 History", use_container_width=True, type="secondary"):
            st.session_state.show_chat_history = not st.session_state.get("show_chat_history", False)
            st.rerun()

    # ── Chat History Sidebar / View ────────────────────────────────────────────
    if st.session_state.get("show_chat_history", False):
        st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
        st.subheader("📜 Saved Chat History")
        chat_sessions = db_service.list_chat_sessions()
        if not chat_sessions:
            st.info("No saved chat sessions yet!")
        else:
            for i, session in enumerate(chat_sessions):
                with st.expander(f"Chat {i+1} - {session['created_at'][:10]}"):
                    for msg in session["history"]:
                        with st.chat_message(msg["role"]):
                            st.markdown(msg["content"])
                    if st.button(f"Load Chat {i+1}", key=f"load_{i}", use_container_width=True):
                        st.session_state.chatbot_history = session["history"]
                        st.session_state.current_chat_session_id = session["id"]
                        st.session_state.show_chat_history = False
                        st.rerun()
                    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    # ── API key status ────────────────────────────────────────────────────────
    api_key = st.session_state.get("gemini_api_key", "").strip()
    if not api_key:
        st.warning(
            "⚠️ No Gemini API key configured — chatbot is in offline mode. "
            "Enter your key under ⚙️ Settings to unlock full AI responses."
        )
    else:
        st.success("✅ Gemini API connected — full AI responses active.")

    # ── Handle redirect query from Opportunities page ─────────────────────────
    incoming = st.session_state.pop("chatbot_query", None)
    if incoming:
        st.session_state.chatbot_history.append({"role": "user", "content": incoming})
        with st.chat_message("user"):
            st.markdown(incoming)
        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                agent = _make_agent()
                res = agent.run({
                    "message":      incoming,
                    "history":      st.session_state.chatbot_history[:-1],
                    "user_context": _user_context(),
                })
                reply = res.get("response", "Sorry, I couldn't process that.")
                st.markdown(reply)
        st.session_state.chatbot_history.append({"role": "assistant", "content": reply})
        st.rerun()

    # ── Render conversation history ───────────────────────────────────────────
    for msg in st.session_state.chatbot_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ── Chat input ────────────────────────────────────────────────────────────
    user_input = st.chat_input(
        "Ask about your roadmap, certifications, interview prep, resume gaps…"
    )
    if user_input:
        st.session_state.chatbot_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                agent = _make_agent()
                res = agent.run({
                    "message":      user_input,
                    "history":      st.session_state.chatbot_history[:-1],
                    "user_context": _user_context(),
                })
                reply = res.get("response", "Sorry, I couldn't process that.")
                st.markdown(reply)
        st.session_state.chatbot_history.append({"role": "assistant", "content": reply})
        st.rerun()