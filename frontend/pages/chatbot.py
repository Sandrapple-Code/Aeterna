import streamlit as st
from services.llm_service import LLMService
from services.db_service import DBService
from agents.chatbot_agent import ChatbotAgent


def render_chatbot_page() -> None:
    """
    Renders the Chatbot page with history and fresh chat options.
    """
    # Initialize chat history
    if "chatbot_history" not in st.session_state:
        st.session_state.chatbot_history = []

    # Page header with home and fresh chat buttons
    col_home, col_title, col_action = st.columns([1, 4, 1.5])
    with col_home:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_page = "Landing"
            st.rerun()
    with col_title:
        st.markdown('<div class="dashboard-title">💬 Chatbot</div>', unsafe_allow_html=True)
        st.markdown('<div class="dashboard-subtitle">Ask questions about your career</div>', unsafe_allow_html=True)
    with col_action:
        if st.button("🔄 Fresh Chat", use_container_width=True, type="primary"):
            st.session_state.chatbot_history = []
            if "chatbot_query" in st.session_state:
                del st.session_state.chatbot_query
            st.success("Started a new chat session!")
            st.rerun()

    # If there's an incoming query redirect from Opportunities, process it
    incoming_query = st.session_state.get("chatbot_query")
    if incoming_query:
        # Clear the incoming query so we don't loop
        del st.session_state.chatbot_query
        
        # Add to history
        st.session_state.chatbot_history.append({"role": "user", "content": incoming_query})
        
        # Process response immediately
        with st.chat_message("user"):
            st.markdown(incoming_query)
            
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                llm = LLMService()
                api_key = st.session_state.get("gemini_api_key")
                if api_key and "dummy" not in api_key.lower() and "mock" not in api_key.lower():
                    from google import genai
                    llm.client = genai.Client(api_key=api_key)
                db = DBService()
                agent = ChatbotAgent(llm, db)
                result = agent.run({
                    "message": incoming_query,
                    "history": st.session_state.chatbot_history[:-1]
                })
                response = result.get("response", "I couldn't process that right now.")
                st.markdown(response)
        
        st.session_state.chatbot_history.append({"role": "assistant", "content": response})
        st.rerun()

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
                api_key = st.session_state.get("gemini_api_key")
                if api_key and "dummy" not in api_key.lower() and "mock" not in api_key.lower():
                    from google import genai
                    llm.client = genai.Client(api_key=api_key)
                db = DBService()
                agent = ChatbotAgent(llm, db)
                result = agent.run({
                    "message": user_input,
                    "history": st.session_state.chatbot_history[:-1]
                })
                
                response = result.get("response", "Sorry, I couldn't process that right now.")
                st.markdown(response)
                
        st.session_state.chatbot_history.append({"role": "assistant", "content": response})
        st.rerun()
