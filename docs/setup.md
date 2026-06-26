# Aeterna – Local Setup & Deployment Guide

This guide walks you through setting up, configuring, running, and deploying the **Aeterna Career Operating System** on your local machine and to production cloud environments.

---

## 💻 Local Development Setup

Follow these step-by-step instructions to get the application running locally.

### 1. Clone & Prepare Directory
Clone the repository and navigate to the project root:
```bash
git clone <your-repository-url> Aeterna
cd Aeterna
```

### 2. Configure Python Virtual Environment
Always run python applications inside a isolated virtual environment to prevent package collision.

- **Create a virtual environment (`.venv`):**
  ```bash
  python -m venv .venv
  ```
- **Activate the environment:**
  - **Windows (PowerShell):**
    ```powershell
    .venv\Scripts\Activate.ps1
    ```
  - **macOS/Linux:**
    ```bash
    source .venv/bin/activate
    ```

### 3. Install Required Dependencies
Install all production and development dependencies using the explicit environment path:
```bash
.venv/bin/pip install -r requirements.txt
```

### 4. Set Up Environment Secrets
1. Copy the environment configuration template:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` in your preferred editor.
3. Obtain a Gemini API Key:
   - Go to [Google AI Studio](https://aistudio.google.com/).
   - Click **Get API Key** and create a new key.
4. Paste the key into your `.env` file:
   ```env
   GEMINI_API_KEY=AIzaSyD...Your_Actual_Gemini_Key
   ```

### 5. Start the Streamlit Application
Execute the Streamlit server from the active virtual environment:
```bash
.venv/bin/streamlit run app.py
```
A browser tab should open automatically to [http://localhost:8501](http://localhost:8501).

---

## 🔍 Code Validation & Syntax Checks

Before committing changes, check that there are no broken imports or compilation errors.

### 1. Dry-Run Import Check
You can run a dry import check using python directly:
```bash
.venv/bin/python -c "import app; print('Imports compiled successfully!')"
```

### 2. Run Automated Syntax / Testing (Optional)
If you add tests inside a `tests/` folder later, you can run them using:
```bash
.venv/bin/pytest
```

---

## ☁️ Deployment Guide (Streamlit Community Cloud)

Streamlit Community Cloud is the easiest way to deploy and share Aeterna for free.

### Step 1: Push Code to GitHub
Ensure all your files (excluding those in `.gitignore`) are committed and pushed to GitHub:
```bash
git add .
git commit -m "feat: scaffold production-ready clean architecture"
git push origin main
```

### Step 2: Set Up Streamlit Cloud Account
1. Visit [share.streamlit.io](https://share.streamlit.io/).
2. Sign in with your GitHub account.

### Step 3: Configure Deployment
1. Click **New App** in your Streamlit dashboard.
2. Select your repository (`Aeterna`), branch (`main`), and set the Main file path to `app.py`.
3. Click on the **Advanced Settings** button.
4. Under **Secrets**, paste the contents of your `.env` file in TOML format:
   ```toml
   APP_ENV = "production"
   LOG_LEVEL = "INFO"
   GEMINI_API_KEY = "AIzaSyD...Your_Actual_Gemini_Key"
   DATABASE_URL = "sqlite:///./aeterna.db"
   SECRET_KEY = "a_secure_production_only_secret_string"
   ```
5. Click **Save** and then click **Deploy**.

Streamlit will provision a container, install packages from `requirements.txt`, configure environmental secrets, and make your application live under a public URL!
