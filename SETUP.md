# Setup Guide for Job Application Helper

This guide will help you get the application running with proper configuration.

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- A text editor

## Step 1: Clone or Download the Repository

```bash
git clone <repository-url>
cd ApplicationHelper
```

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 3: Configure Environment Variables

### Create Your `.env` File

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and add your configuration:
   ```
   GROQ_API_KEY=your_actual_groq_api_key
   GOOGLE_SHEETS_ID=your_sheet_id
   GOOGLE_SHEETS_NAME=Internships
   LINKEDIN_URL=https://www.linkedin.com/in/your-profile/
   SCHOOL=Your School Name
   GITHUB_URL=https://github.com/your-username
   PAST_JOB=Your Company Name
   ```

### Getting Your API Keys

#### Groq API Key (Free)
1. Visit [console.groq.com/keys](https://console.groq.com/keys)
2. Sign up or log in
3. Create a new API key
4. Copy the key and paste it into your `.env` file

#### Google Sheets Integration (Optional)

If you want to automatically log applications to Google Sheets:

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable the **Google Sheets API** and **Google Drive API**
4. Go to **Credentials** → **Create Credentials** → **OAuth 2.0 Desktop Application**
5. Download the JSON file
6. Save it in your ApplicationHelper folder as `client_secret_*.json`
7. Find your Google Sheet ID:
   - Open your Google Sheet
   - The URL looks like: `https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit`
   - Copy the `{SHEET_ID}` portion
8. Add it to your `.env` file

## Step 4: Add Your Resume

Create a `resume.txt` file in the ApplicationHelper folder with your resume content.

## Step 5: Run the Application

```bash
python main.py
```

## Troubleshooting

### "ModuleNotFoundError" when running the app
- Make sure you've run `pip install -r requirements.txt`
- Try running `pip install python-dotenv groq pyperclip` individually

### API Key not working
- Double-check that your `.env` file is in the same directory as `config.py`
- Make sure there are no extra spaces in your `.env` file values
- Verify your API keys are correct and haven't expired

### Can't load resume
- Make sure `resume.txt` is in the ApplicationHelper folder
- The file should be readable as UTF-8 text

### Google Sheets not syncing
- Verify your `GOOGLE_SHEETS_ID` is correct
- Check that your `client_secret_*.json` file is in the correct folder
- On first run, you may be prompted to authorize the application

## Security Notes

- ⚠️ **Never commit your `.env` file to version control**
- ⚠️ **Never share your `.env` file**
- ⚠️ **Never commit `client_secret_*.json` files**
- These files are listed in `.gitignore` to prevent accidental commits
- If you accidentally commit secrets, you must regenerate them

## Building a Standalone Executable

To create a standalone app (no Python required to run):

```bash
python build_app.py
```

The built application will be in the `dist/` folder:
- **macOS**: `Application Helper.app`
- **Windows**: `Application Helper.exe`

## Support

If you encounter issues:
1. Check the `.env.example` file for the correct format
2. Verify all API keys are valid
3. Make sure all dependencies are installed
4. Check that Python 3.9+ is being used

---

**Ready to use?** Run `python main.py` and start streamlining your job applications! 🚀
