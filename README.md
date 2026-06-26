# Aeterna – The Career Operating System 🚀

Powered by the **CareerForge Engine**, **Aeterna** is a production-ready, AI-powered career optimization and management suite. It serves as a comprehensive cockpit for job seekers, helping them optimize their resume, prepare for interviews with realistic AI-driven coaching, and chart their long-term career progression.

---

## 🏗️ Project Architecture

Aeterna is built following **Clean Architecture** principles. The codebase is organized to enforce a strict separation of concerns, ensuring that the application remains modular, easy to test, and highly extensible as new AI agents and data sources are integrated.

```
Aeterna/
├── .env.example            # Template for environment variables
├── .gitignore              # Git ignore rules
├── README.md               # Main documentation
├── app.py                  # Main Streamlit entry point & routing
├── requirements.txt        # Python dependency list
├── config/                 # Configuration & setting modules
│   ├── __init__.py
│   └── settings.py         # Type-safe configuration loading
├── agents/                 # AI Agent layer (CareerForge Engine)
│   ├── __init__.py
│   ├── base_agent.py       # Abstract base class for all agents
│   ├── resume_optimizer.py # Resume analysis & tailored optimization agent
│   ├── interview_coach.py  # Behavioral & technical mock interview agent
│   └── career_pathfinder.py# Career transition & path mapping agent
├── services/               # Core business services & integration layer
│   ├── __init__.py
│   ├── llm_service.py      # LLM client wrapper (Google GenAI / Gemini)
│   ├── db_service.py       # Data storage & retrieval client interface
│   └── pdf_service.py      # PDF Resume / Report builder service
├── frontend/               # Streamlit Presentation Layer
│   ├── __init__.py
│   ├── components/         # Reusable UI widgets and elements
│   │   ├── __init__.py
│   │   ├── cards.py        # Styled layout cards (CSS-backed)
│   │   └── sidebar.py      # Sidebar state and navigation controller
│   ├── pages/              # Module-specific view templates
│   │   ├── __init__.py
│   │   ├── dashboard.py    # Main user cockpit
│   │   ├── interview_prep.py# Mock interview practice console
│   │   └── resume_studio.py# Tailoring studio
│   └── styles/
│       └── custom.css      # Premium typography, theme overrides, glassmorphism
├── utils/                  # Helper modules and utilities
│   ├── __init__.py
│   ├── helpers.py          # String, file, and dictionary formatting
│   └── logger.py           # Loguru-powered centralized logger
├── prompts/                # Prompt Engineering & system instructions
│   ├── __init__.py
│   └── templates.py        # Structured prompts for CareerForge Agents
├── assets/                 # Static visual assets (logos, illustrations)
│   └── .gitkeep
├── reports/                # Local storage directory for compiled PDFs
│   └── .gitkeep
└── docs/                   # Full-length technical and architectural docs
    ├── architecture.md     # Detailed architecture documentation
    └── setup.md            # Thorough environment setup guide
```

---

## 💎 Design Philosophy & User Experience (UX)

Aeterna features a **premium glassmorphism theme** built on top of Streamlit.
- **Visual Excellence**: Custom styling (`frontend/styles/custom.css`) overrides standard Streamlit elements with smooth gradients, soft border-shadows, and elegant dark-mode cards.
- **Dynamic Feedback**: Implements subtle micro-animations, active hover transitions, and intuitive feedback loops for AI response loading states.
- **Modular Navigation**: Controlled via a specialized sidebar component (`frontend/components/sidebar.py`) that synchronizes session states seamlessly across pages.

---

## ⚡ Getting Started

### Prerequisites
- Python 3.10 or higher installed.
- A Google AI Studio API Key (for Gemini models).

### 1. Clone & Set Up Directory
Navigate to your workspace directory:
```bash
cd Aeterna
```

### 2. Initialize Virtual Environment
Create a clean local virtual environment:
```bash
python -m venv .venv
```
Activate the environment:
- **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
- **macOS/Linux:**
  ```bash
  source .venv/bin/activate
  ```

### 3. Install Dependencies
Install production-ready packages using the explicit path:
```bash
.venv/bin/pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to a new `.env` file:
```bash
cp .env.example .env
```
Open `.env` and configure your settings:
```ini
GEMINI_API_KEY=AIzaSy...Your_Actual_Gemini_Key_Here
```

### 5. Run the Application
Start the Streamlit server:
```bash
.venv/bin/streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## ☁️ Deployment on Streamlit Community Cloud

Aeterna is fully prepared for zero-configuration deployment on **Streamlit Community Cloud**:
1. Push this repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io/) and connect your GitHub account.
3. Select your repository, branch, and set the entry point file to `app.py`.
4. Under **Advanced Settings**, add your environment variables (from `.env`) to the **Secrets** section:
   ```toml
   GEMINI_API_KEY = "your_actual_api_key_here"
   APP_ENV = "production"
   LOG_LEVEL = "INFO"
   DATABASE_URL = "sqlite:///./aeterna.db"
   SECRET_KEY = "your_secure_production_secret"
   ```
5. Click **Deploy!**

---

## 📄 License
This project is proprietary and confidential. Powered by the **CareerForge Engine**.

This is a test from Trae.