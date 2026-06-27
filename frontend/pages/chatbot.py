import streamlit as st
from services.llm_service import LLMService
from services.db_service import DBService
from agents.chatbot_agent import ChatbotAgent


def render_chatbot_page() -> None:
    """
    Renders the Chatbot page
    """
    # Page header with home button
    col_home, col_title = st.columns([1, 5])
    with col_home:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_page = "Landing"
            st.rerun()
    with col_title:
        st.markdown('<div class="dashboard-title">💬 Chatbot</div>', unsafe_allow_html=True)
        st.markdown('<div class="dashboard-subtitle">Ask questions about your career</div>', unsafe_allow_html=True)
        
    # Initialize chat history
    if "chatbot_history" not in st.session_state:
        st.session_state.chatbot_history = []
        
    # Render chat history
    for message in st.session_state.chatbot_history:
        role = message["role"]
        with st.chat_message(role):
            st.markdown(message["content"])
            
    # Chat input
    user_input = st.chat_input("Ask a question about your career...")
    if user_input:
        # Add user message to history
        st.session_state.chatbot_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
            
        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                llm = LLMService()
                db = DBService()
                agent = ChatbotAgent(llm, db)
                result = agent.run({"message": user_input})
                
                response = result.get("response", "Sorry, I couldn't process that right now.")
                st.markdown(response)
                
        st.session_state.chatbot_history.append({"role": "assistant", "content": response})
