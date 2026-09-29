# Meeting Prep Agent 🚀

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask_3.x-green.svg)](https://flask.palletsprojects.com/)
[![TailwindCSS](https://img.shields.io/badge/UI-TailwindCSS-38bdf8.svg)](https://tailwindcss.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Mobile Friendly](https://img.shields.io/badge/Mobile-Responsive-success.svg)](#-mobile-phone-access)

An intelligent, executive-grade meeting preparation dashboard designed to help founders, managers, consultants, and professionals walk into every meeting prepared, confident, and focused on outcomes.

---

## ✨ Features

- **Intuitive Meeting Intake Form**:
  - Meeting title
  - Person / Company name
  - Meeting date and time
  - Meeting purpose
  - Previous meeting notes
  - Additional information
- **7-Part Executive Briefing Dossier**:
  - 🎯 **Meeting Objective**: Primary objective & measurable success criteria.
  - 🏢 **Person / Company Summary**: Stakeholder context, relationship background, and synthesized dynamics.
  - 📋 **Key Discussion Points**: Prioritized agenda with suggested time blocks (5m, 10m, 20m).
  - ❓ **Important Questions to Ask**: High-leverage discovery, clarification, and closing questions.
  - 💬 **Suggested Talking Points**: Strategic talking tracks, value propositions, and direct references to past notes.
  - 🛡️ **Possible Concerns or Objections**: Anticipated pushback paired with actionable mitigation strategies.
  - ⏩ **Recommended Next Steps**: Post-meeting action items with owners and deadlines.
- **Productivity & Sharing Tools**:
  - 📱 **Mobile Phone Access**: Scan QR code to run and view briefs directly on your smartphone.
  - 📥 **Download `.MD`**: Save complete formatted markdown briefs with one click to store in Notion, Obsidian, or Google Drive.
  - 📅 **Add to Calendar (`.ics`)**: Exports a standard calendar invite file for Microsoft Outlook, Apple Calendar, or Google Calendar.
  - 📋 **Copy to Clipboard (Markdown)**: Instant paste format for Slack or email.
  - 🖨️ **Print / PDF**: Professional `@media print` layout styled as an executive briefing memo.
  - ✉️ **Follow-up Email Template**: Pre-formatted, ready-to-send post-meeting email template.
  - ⚡ **Pre-loaded Quick Presets**: Enterprise Sales Pitch, 1-on-1 Review, Client Kickoff, Investor Review.
  - 💾 **SQLite History & Search**: Save, browse, reload, and delete past briefs with offline persistence.
  - 🌓 **Dark / Light Mode Toggle**.

---

## 📱 Mobile Phone Access

You can use Meeting Prep Agent directly on your smartphone:

### Option A: Local Wi-Fi (Same Network)
1. Ensure your phone is connected to the same Wi-Fi network as your computer.
2. Click **"Phone"** in the top navbar on your computer to reveal the live **QR code**.
3. Scan the QR code with your phone camera, or open:
   ```
   http://<YOUR_COMPUTER_LOCAL_IP>:8080
   ```

### Option B: Cellular Data (4G/5G) / Remote Access
Double-click [`share_to_phone.bat`](share_to_phone.bat) on your computer. It uses built-in Windows SSH to create a secure public `https://...` link you can open anywhere in the world!

---

## 🚀 Quick Start (Local Setup)

### 1. Prerequisites
- Python 3.10 or higher
- Git

### 2. Clone & Install
```bash
git clone https://github.com/<your-username>/meeting-prep-agent.git
cd meeting-prep-agent

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the App
```bash
python app.py
```
Open your browser and navigate to:
```
http://localhost:8080
```
*(On Windows, you can also double-click `run.bat`)*

---

## 🐙 How to Push this Project to GitHub

Follow these simple steps in terminal or PowerShell from the project folder:

```bash
# 1. Initialize git
git init

# 2. Add all files
git add .

# 3. Create your first commit
git commit -m "Initial commit: Meeting Prep Agent web application"

# 4. Create a new repository on https://github.com/new named 'meeting-prep-agent'

# 5. Link your local project to GitHub and push (replace <your-username>)
git remote add origin https://github.com/<your-username>/meeting-prep-agent.git
git branch -M main
git push -u origin main
```

---

## 🌐 Free Cloud Deployment (Optional)

This app is production-ready for deployment to free platforms:

### Deploy to Render
1. Push this repository to GitHub.
2. Go to [render.com](https://render.com/) -> **New Web Service**.
3. Select your repository.
4. Settings:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app` (or `python app.py`)
5. Click **Deploy**!

---

## 📂 Project Structure

```
meeting-prep-agent/
├── app.py              # Flask server and REST API endpoints
├── database.py         # SQLite persistence manager for meetings and briefs
├── generator.py        # Context-aware briefing synthesis engine
├── samples.py          # Pre-loaded meeting scenarios for 1-click testing
├── test_app.py         # Automated unit & integration test suite
├── requirements.txt    # Project dependencies
├── .gitignore          # Git exclusion rules
├── run.bat             # 1-click Windows desktop launcher
├── share_to_phone.bat  # 1-click mobile phone sharing script
├── start_app.ps1       # PowerShell launcher
├── templates/
│   └── index.html      # Responsive dashboard with QR code modal & history
├── static/
│   ├── css/
│   │   └── style.css   # Custom typography, animations & PDF print styling
│   └── js/
│       └── app.js      # Client controller, async API, history, copy/print
└── README.md           # Documentation
```

---

## 🧪 Testing

Run the automated test suite:
```bash
python test_app.py
```

---

## 📄 License

MIT License. Free for personal and commercial use.
