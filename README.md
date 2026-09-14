# Job Application Helper

A Python-based desktop application designed to streamline your job application process with AI-powered assistance.

## Features

- **Automated ATS Keyword Extraction**: AI automatically extracts relevant keywords from job descriptions
- **AI Question Answering**: Get AI-drafted answers tailored to your resume and job description  
- **Cover Letter Generation**: Auto-generate customized cover letters with company research
- **Google Sheets Sync**: Auto-log applications to your tracking sheet
- **Split-Screen Workflow**: Optimized for side-by-side use while applying to jobs

---

## Quick Start

### macOS

**Easiest way to run:**
```bash
cd ~/ApplicationHelper
python3 main.py
```

**To make it a clickable app (no terminal needed):**

1. Create a shortcut file:
```bash
cat > ~/Desktop/ApplicationHelper.command << 'EOF'
#!/bin/bash
cd ~/ApplicationHelper && python3 main.py
EOF
chmod +x ~/Desktop/ApplicationHelper.command
```

2. Double-click the `ApplicationHelper.command` file on your desktop to run!

---

### Windows

**Prerequisites:**
1. Install Python 3.9+ from [python.org](https://www.python.org/downloads/)
   - ✅ **CHECK: "Add Python to PATH"** during installation
   
2. Open Command Prompt and run:
```cmd
pip install groq google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

**To run the app:**
```cmd
cd C:\path\to\ApplicationHelper
python main.py
```

**To make it a clickable app (no Command Prompt needed):**

1. Create a batch file:
   - Open Notepad
   - Paste:
   ```batch
   @echo off
   cd C:\path\to\ApplicationHelper
   python main.py
   pause
   ```
   - Save as `ApplicationHelper.bat` in your ApplicationHelper folder

2. Right-click the .bat file → **Send to** → **Desktop (create shortcut)**

3. Double-click the desktop shortcut to run!

---

## Setup & Configuration

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

1. **Copy the template file:**
   ```bash
   cp .env.example .env
   ```

2. **Get your API keys:**
   - **Groq API** (Free): Get at [console.groq.com/keys](https://console.groq.com/keys)
   - **Google Sheets Integration** (Optional):
     1. Go to [Google Cloud Console](https://console.cloud.google.com)
     2. Create a project, enable Google Sheets API
     3. Create OAuth 2.0 Desktop App credentials
     4. Download the JSON file and save it in your ApplicationHelper folder as `client_secret_*.json`
     5. Get your Google Sheet ID (found in the sheet's URL: `docs.google.com/spreadsheets/d/{SHEET_ID}/`)

3. **Edit `.env` file with your information:**
   ```
   GROQ_API_KEY=your_groq_api_key_here
   GOOGLE_SHEETS_ID=your_sheet_id_here
   GOOGLE_SHEETS_NAME=Internships
   LINKEDIN_URL=https://www.linkedin.com/in/your-profile/
   SCHOOL=Your School Name
   GITHUB_URL=https://github.com/your-username
   PAST_JOB=Your Company Name
   ```

### 3. Prepare Your Files

Place these in your ApplicationHelper folder:
- `resume.txt` - Your resume content
- `client_secret_*.json` - Your Google OAuth credentials file (if using Google Sheets)
- `.env` - Environment variables (created above, never commit this!)

### ⚠️ Important: Never Commit `.env`

The `.env` file contains your API keys and should **never** be committed to version control. It's already listed in `.gitignore` to prevent accidental commits.

## Usage

Run the application:
```bash
python main.py
```

### Workflow

1. **Top Bar Buttons**: Click any button to copy your info
2. **Paste Job Description**: Paste the job description - ATS keywords will extract automatically
3. **Paste Job Link**: Add the job posting link
4. **Answer Questions**: Ask questions and get AI-drafted answers
5. **Generate Cover Letter**: Create a customized cover letter
6. **Submit**: Push to Google Sheets and reset for the next application

## Project Structure

```
ApplicationHelper/
├── main.py                          # Main application file
├── config.py                        # Configuration (user data)
├── requirements.txt                 # Python dependencies
├── templates/
│   └── cover_letter_template.txt   # Cover letter template
└── README.md                        # This file
```

## Coming Soon

- Gemini API integration for ATS keyword extraction
- LLM integration for answer generation
- Google Sheets API integration
- Desktop notifications/toast messages
- Cover letter generation to Downloads folder

## Notes

- The app is optimized for 1200x800 window size
- Best used as a split-screen tool alongside job posting websites
- All data is stored locally; no cloud sync (except Google Sheets submission)
