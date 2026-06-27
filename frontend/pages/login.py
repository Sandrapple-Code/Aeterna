import streamlit as st

def render_login_page() -> None:
    """
    Renders a premium glassmorphic authentication page.
    """
    st.markdown(
        """
        <div style="text-align: center; padding: 60px 0 20px 0;">
            <h1 style="font-family: 'Outfit', sans-serif; font-size: 3.5rem; font-weight: 800; 
                       background: linear-gradient(135deg, #38bdf8 0%, #a855f7 100%);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                       margin-bottom: 0px;">
                Aeterna
            </h1>
            <p style="color: #64748b; font-size: 1rem; letter-spacing: 0.05em; text-transform: uppercase; margin-top: 5px;">
                Career Operating System
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown(
            """
            <div class="aeterna-card" style="padding: 30px;">
                <h3 style="text-align: center; margin-bottom: 25px; color: #f8fafc;">🔐 Sign In to Aeterna</h3>
            """, 
            unsafe_allow_html=True
        )
        
        username = st.text_input("Username", placeholder="Enter username (e.g. admin)", key="login_user")
        password = st.text_input("Password", type="password", placeholder="Enter password (e.g. password123)", key="login_pass")
        
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        
        if st.button("Access Dashboard", type="primary", use_container_width=True):
            if username.strip() and password.strip():
                st.session_state.logged_in = True
                st.session_state.username = username.strip()
                
                # Initialize name in intake data to the username
                if "intake_data" not in st.session_state:
                    st.session_state.intake_data = {}
                st.session_state.intake_data["name"] = username.strip()
                
                st.success("Successfully logged in!")
                st.rerun()
            else:
                st.error("Please enter both username and password.")
                
        st.markdown("</div>", unsafe_allow_html=True)
