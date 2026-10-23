# Ultimate Tetris: Mobile-Optimized Arcade Engine

A professional, high-performance clone of the classic Tetris arcade game built using Python and Streamlit. This application transforms a traditionally stateless data dashboard framework into a real-time reactive game engine, featuring wall-kicks, hard drops, matrix rotation, and dynamic speed scaling.

---

## Project Architecture

```text
tetris-app/
│
├── .streamlit/
│   └── config.toml       # Streamlit theme and layout configurations
├── streamlit_app.py      # Main Application & Game Engine Logic
├── requirements.txt      # List of core dependencies
├── .gitignore            # Excludes temporary files from version control
└── README.md             # Project documentation
```

---

## Prerequisites

Before running this project, ensure you have the following installed on your system:
* **Python 3.8+** - Required to execute the Streamlit execution loop.
* **Pip** - Python package manager for handling dependencies.

---

## Local Installation and Execution

### Step 1: Clone and Install Dependencies
1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
   ```
2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Step 2: Run the Application
1. Launch the Streamlit application from the root directory:
   ```bash
   streamlit run streamlit_app.py
   ```
2. Open the local URL provided in your terminal (typically `http://localhost:8501`) to play the game in your browser.

---

## Deployment on Streamlit Community Cloud

To deploy this mobile-optimized arcade game publicly using Streamlit Community Cloud:

1. Push your repository to **GitHub**, ensuring that `streamlit_app.py` and `requirements.txt` are included in the root directory.
2. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
3. Click **Create app** and configure the deployment settings:
   * **Repository:** Select your Tetris repository.
   * **Branch:** `main` (or your default branch)
   * **Main file path:** `streamlit_app.py`
4. Click **Deploy**. No external API secrets are required for this project.