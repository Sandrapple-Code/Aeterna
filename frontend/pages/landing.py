import streamlit as st
from frontend.components.cards import render_card


def render_landing_page() -> None:
    """
    Renders the Aeterna Premium Landing Page.
    """
    # Initialize settings panel state
    if "show_settings" not in st.session_state:
        st.session_state.show_settings = False

    # Hero Section
    st.markdown("""
    <div style="text-align: center; padding: 80px 20px;">
        <div class="aeterna-badge" style="font-size: 0.85rem; margin-bottom: 24px;">🌌 Career Operating System</div>
        <h1 style="font-size: 3.5rem; font-weight: 800; margin-bottom: 12px; background: linear-gradient(135deg, #38bdf8 0%, #a855f7 50%, #ec4899 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-family: 'Outfit', sans-serif;">
            Aeterna
        </h1>
        <h2 style="font-size: 2rem; font-weight: 700; margin-bottom: 16px; color: #f8fafc; font-family: 'Outfit', sans-serif;">
            The Career Operating System
        </h2>
        <p style="font-size: 1.1rem; color: #94a3b8; margin-bottom: 12px; font-weight: 500;">
            Powered by the CareerForge Engine
        </p>
        <p style="font-size: 1rem; color: #cbd5e1; max-width: 800px; margin: 0 auto 40px; line-height: 1.7;">
            Discover the right career, identify your skill gaps, build personalized learning roadmaps, optimize your resume, and uncover real-world opportunities using specialized AI agents.
        </p>
        <p style="margin-top: 20px; color: #64748b; font-size: 0.9rem;">Discover. Plan. Achieve.</p>
    </div>
    """, unsafe_allow_html=True)

    # Launch Button (primary CTA) - Centered, glassmorphism style
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Custom CSS to turn the primary button into a blue-purple gradient
        st.markdown(
            """
            <style>
            button[kind="primary"] {
                background: linear-gradient(90deg, #4F9DFF 0%, #A06CFF 100%);
                border: none;
                color: white;
                transition: transform 0.2s ease, box-shadow 0.2s ease, opacity 0.2s ease;
                box-shadow: 0 0 0 rgba(79, 157, 255, 0);
            }
            button[kind="primary"]:hover {
                opacity: 0.95;
                color: white;
                transform: translateY(-3px) scale(1.03);
                box-shadow:
                     0 0 3px 2px rgba(79, 157, 255, 0.2),
                     
                     0 8px 20px rgba(0, 0, 0, 0.3);
            }
            button[kind="primary"]:active {
                transform: translateY(-1px) scale(1.01);
            }

            /* Neon glow hover for cards (e.g. Career Match) — overrides external stylesheet */
            .aeterna-card:hover {
                transform: translateY(-4px) !important;    }
            </style>
            """,
            unsafe_allow_html=True,
        
        )
        if st.button(
            "🚀 Launch Career Analysis",
            key="hero-launch",
            type="primary",
            use_container_width=True
        ):
            # Check if API key exists in session state
            if not st.session_state.get("gemini_api_key"):
                st.session_state.show_settings = True
                st.rerun()
            else:
                st.session_state.current_page = "Career Discovery"
                st.rerun()

        # Settings Expandable Panel
        if st.session_state.show_settings:
            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
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
                    <b>Important:</b> Your API keys are stored <b>only in your current browser session</b> and are never saved to disk or transmitted to any third-party servers except when making direct API calls to the respective AI services. When you close this tab or refresh the page, your API key will be cleared.
                    """
                )
                if st.button("Close Settings", use_container_width=True):
                    st.session_state.show_settings = False
                    st.rerun()

    # About Aeterna Section
    st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 40px;">
        <h2 style="font-size: 2.2rem; font-weight: 700; color: #f8fafc; margin-bottom: 12px;">About Aeterna</h2>
        <p style="color: #94a3b8; font-size: 1.05rem;">Your all-in-one career companion</p>
    </div>
    """, unsafe_allow_html=True)

    render_card(
        title="For Everyone, Every Step of the Way",
        body="""
        Aeterna is designed to help <b>students, graduates, working professionals, and career switchers</b> navigate their career journey with confidence.
        Our platform combines multiple AI agents working together to deliver personalized, actionable guidance tailored to your unique goals.
        """
    )

    # Meet Your AI Team Section
    st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 40px;">
        <h2 style="font-size: 2.2rem; font-weight: 700; color: #f8fafc; margin-bottom: 12px;">Meet Your AI Team</h2>
        <p style="color: #94a3b8; font-size: 1.05rem;">Specialized agents working for your success</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        render_card(
            title="🧠 Career Discovery Agent",
            body="Finds the most suitable career path based on interests, education, goals, and skills."
        )
        render_card(
            title="📚 Career Planner Agent",
            body="Builds personalized learning roadmaps, identifies skill gaps, recommends projects, and prepares users for interviews."
        )
    with col2:
        render_card(
            title="📄 Resume Intelligence Agent",
            body="Analyzes resumes, identifies missing skills, ATS improvements, and optimization opportunities."
        )
        render_card(
            title="🌍 Opportunity Agent",
            body="Discovers internships, jobs, hackathons, fellowships, and career opportunities tailored to the user's goals."
        )

    # How Aeterna Works Section
    st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 40px;">
        <h2 style="font-size: 2.2rem; font-weight: 700; color: #f8fafc; margin-bottom: 12px;">How Aeterna Works</h2>
        <p style="color: #94a3b8; font-size: 1.05rem;">Your journey to career success in 6 simple steps</p>
    </div>
    """, unsafe_allow_html=True)

    steps = [
        ("Tell us about yourself", "Step 1"),
        ("AI analyzes your profile", "Step 2"),
        ("Resume Analysis (optional)", "Step 3"),
        ("Personalized Career Roadmap", "Step 4"),
        ("Discover Opportunities", "Step 5"),
        ("Download Your Career Report", "Step 6")
    ]

    for i, (step_text, step_label) in enumerate(steps):
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 20px; margin: 20px 0;">
            <div style="
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background: linear-gradient(135deg, #38bdf8 0%, #a855f7 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.5rem;
                font-weight: 800;
                color: white;
                font-family: 'Outfit', sans-serif;
                flex-shrink: 0;
            ">
                {i + 1}
            </div>
            <div style="flex-grow: 1;">
                <div style="font-family: 'Outfit', sans-serif; font-size: 0.85rem; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">{step_label}</div>
                <div style="font-size: 1.25rem; font-weight: 700; color: #f8fafc; font-family: 'Outfit', sans-serif;">{step_text}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if i < len(steps) - 1:
            st.markdown("<div style='text-align: center; font-size: 1.5rem; color: #64748b; margin: 10px 0;'>↓</div>", unsafe_allow_html=True)

    # Why Choose Aeterna Section
    st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 40px;">
        <h2 style="font-size: 2.2rem; font-weight: 700; color: #f8fafc; margin-bottom: 12px;">Why Choose Aeterna</h2>
        <p style="color: #94a3b8; font-size: 1.05rem;">What sets us apart</p>
    </div>
    """, unsafe_allow_html=True)

    features = [
        ("Personalized AI Guidance", "✅"),
        ("Multi-Agent Intelligence", "✅"),
        ("Career Readiness Score", "✅"),
        ("Resume Optimization", "✅"),
        ("Skill Gap Analysis", "✅"),
        ("Internship & Job Discovery", "✅")
    ]

    col1, col2, col3 = st.columns(3)
    for i, (feature, icon) in enumerate(features):
        with [col1, col2, col3][i % 3]:
            render_card(title=f"{icon} {feature}", body="")

    # Technology Section
    st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 40px;">
        <h2 style="font-size: 2.2rem; font-weight: 700; color: #f8fafc; margin-bottom: 12px;">Technology Stack</h2>
        <p style="color: #94a3b8; font-size: 1.05rem;">Built with modern, powerful tools</p>
    </div>
    """, unsafe_allow_html=True)

    techs = [
        "Python",
        "Streamlit",
        "Gemini AI",
        "Firebase (future-ready)",
        "GitHub",
        "CareerForge Engine"
    ]

    tech_cols = st.columns(len(techs))
    for i, tech in enumerate(techs):
        with tech_cols[i]:
            st.markdown(f"""
            <div class="aeterna-card" style="text-align: center; padding: 20px;">
                <div style="font-family: 'Outfit', sans-serif; font-weight: 700; color: #f8fafc;">{tech}</div>
            </div>
            """, unsafe_allow_html=True)

    # Footer Section
    st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; padding: 40px 20px; border-top: 1px solid rgba(255, 255, 255, 0.05);">
        <p style="color: #94a3b8; font-size: 1rem; margin-bottom: 8px;">© 2026 Aeterna</p>
        <p style="color: #cbd5e1; font-size: 1.1rem; font-weight: 600; font-family: 'Outfit', sans-serif; margin-bottom: 8px;">The Career Operating System</p>
        <p style="color: #64748b; font-size: 0.9rem;">Built with AI to empower students and professionals.</p>
    </div>
    """, unsafe_allow_html=True)