# Deployment Guide: Streamlit Cloud

This guide explains how to deploy the Capstone Placement App to Streamlit Cloud for a public URL.

## Prerequisites

1. GitHub account
2. Streamlit Cloud account (free at https://streamlit.io/cloud)

## Deployment Steps

### 1. Prepare Your Repository

Ensure your GitHub repository has the following structure:

```
DataDivasLena/
├── streamlit_app.py          (main Streamlit app - renamed from gui.py)
├── requirements.txt          (dependencies)
├── README.md                 (documentation)
├── .gitignore               (optional, but recommended)
├── .streamlit/
│   └── config.toml          (optional, Streamlit configuration)
├── datadivas/
│   ├── __init__.py
│   ├── assignment.py        (core optimization logic - UNCHANGED)
│   └── gui.py               (kept for reference)
└── main.py                  (kept for reference)
```

**Note:** The file **must** be named `streamlit_app.py` at the root of the repository for Streamlit Cloud auto-detection.

### 2. Update `requirements.txt`

Ensure `requirements.txt` contains:

```
streamlit==1.28.1
ortools==9.7.2996
pandas==2.1.3
```

### 3. Create `.streamlit/config.toml` (Optional)

This file configures Streamlit settings:

```toml
[theme]
primaryColor = "#FF9500"
backgroundColor = "#111111"
secondaryBackgroundColor = "#1A1A1A"
textColor = "#FFFFFF"
font = "sans serif"

[client]
showErrorDetails = true
```

### 4. Create `.gitignore`

```
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
.idea/
.vscode/
*.swp
*.swo
*~
.DS_Store
.streamlit/secrets.toml
```

### 5. Push to GitHub

```bash
git add .
git commit -m "Convert to Streamlit web app"
git push origin main
```

### 6. Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io
2. Click "New app"
3. Select your GitHub repository
4. Choose the branch (usually "main")
5. Select the script path: `streamlit_app.py`
6. Click "Deploy"

Streamlit will build and deploy your app automatically. You'll get a public URL like:
```
https://yourusername-datadivas-lena.streamlit.app/
```

## Deployment Options Comparison

| Platform | Free Tier | Setup Time | Scale | Best For |
|----------|-----------|-----------|-------|----------|
| **Streamlit Cloud** | Yes (limited) | 5 min | Small-medium | Development, demos |
| **Heroku** | No | 10 min | Small-medium | Production backup |
| **AWS/GCP** | Limited | 20+ min | Any scale | Enterprise |

## Running Locally (Before Deployment)

To test the Streamlit app locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py
```

Then open `http://localhost:8501` in your browser.

## Troubleshooting

### "ModuleNotFoundError: No module named 'datadivas'"

The `datadivas` folder must be in the same directory as `streamlit_app.py` at the root level.

### "ortools installation fails"

On some systems, pre-built OR-Tools wheels may not be available. Ensure you're using Python 3.9+ and try:

```bash
pip install ortools --upgrade
```

### App is slow to load

Streamlit caches results. Initial load can be slow with OR-Tools. Consider:
- Caching optimization results with `@st.cache_data`
- Increasing timeout on Streamlit Cloud (settings)

### Large CSV uploads fail

Streamlit has a 200MB upload limit. For larger datasets, consider:
- Splitting data into multiple runs
- Using a database backend
- Increasing limits in `streamlit_config.toml`

## Environment Variables (Secrets)

For sensitive data (future use):

1. Create a `.streamlit/secrets.toml` file locally (not tracked in git):

```toml
[database]
url = "your_secret_url"
```

2. On Streamlit Cloud, go to App Settings → Secrets and paste the content.

3. Access in code:

```python
import streamlit as st
secret_url = st.secrets["database"]["url"]
```

## Monitoring

Monitor your app via https://share.streamlit.io/admin

Check:
- Performance metrics
- Error logs
- Usage statistics

## Next Steps for Production

For a production deployment, consider:

1. **User Authentication**: Add login with `streamlit-authenticator`
2. **Database**: Store assignments in a database instead of session state
3. **Email Notifications**: Send results to students/faculty
4. **Permissions**: Implement role-based access (admin, faculty, students)
5. **Audit Logging**: Track all assignments for compliance

Example for future auth:

```python
import streamlit as st
from streamlit_authenticator import Authenticate

# Initialize authenticator
# Only allow ECCS chair to run assignments
```

## Support

- Streamlit Cloud docs: https://docs.streamlit.io/deploy/streamlit-cloud
- Streamlit Community: https://discuss.streamlit.io
- OR-Tools: https://developers.google.com/optimization
