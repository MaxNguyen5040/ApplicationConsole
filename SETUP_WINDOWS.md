# Sending Application Helper to Windows

## Quick Steps

### On Your macOS Computer

1. **Gather files to send** (these 7 files):
   - `main.py` - GUI application
   - `llm.py` - LLM & Google Sheets integration
   - `config.py` - Configuration
   - `resume.txt` - Your resume
   - `client_secret_*.json` - Your Google OAuth credentials
   - `run_app.bat` - Windows launcher
   - `README.md` - Instructions

2. **Create a zip file:**
   - Select all 7 files above
   - Right-click → "Compress" (creates a .zip)
   - This creates `Archive.zip`

3. **Send the zip** to your Windows computer via email, cloud drive, USB, etc.

---

## On Your Windows Computer

### Step 1: Install Python (if not already installed)

1. Go to [python.org/downloads](https://www.python.org/downloads)
2. Download Python 3.9 or later
3. **IMPORTANT**: When installing:
   - ✅ Check the box "Add Python to PATH"
   - Click Install Now

4. Verify installation by opening Command Prompt and typing:
   ```cmd
   python --version
   ```

### Step 2: Extract the zip

1. Download the zip file
2. Right-click → "Extract All"
3. Choose where to save (e.g., `C:\Users\YourName\ApplicationHelper`)
4. Remember this path!

### Step 3: Install Python Dependencies

1. Open Command Prompt (search for "cmd" in Windows)
2. Run this command:
   ```cmd
   pip install groq google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```
3. Wait for it to finish (should see "Successfully installed" messages)

### Step 4: Authorize Google

1. Open Command Prompt
2. Navigate to your folder:
   ```cmd
   cd C:\Users\YourName\ApplicationHelper
   ```
3. Run the app once to authorize:
   ```cmd
   python main.py
   ```
4. A browser window will open asking to authorize
5. Click "Allow"
6. Close the window, you can close the app

### Step 5: Create a Desktop Shortcut (Optional but Recommended!)

1. Navigate to your ApplicationHelper folder in File Explorer
2. Right-click on `run_app.bat`
3. Click "Send to" → "Desktop (create shortcut)"
4. A shortcut appears on your desktop!
5. **Now you can just double-click it to run the app** (no Command Prompt needed)

---

## You're Done! 🎉

Your app is now ready to use on Windows. Just:
- **Quick run**: Double-click `run_app.bat` in the ApplicationHelper folder
- **Even quicker**: Double-click the desktop shortcut (if you created one)

---

## Troubleshooting

**"Python not found"**
- Check that Python is installed: `python --version`
- If not, Python wasn't added to PATH. Reinstall and check "Add Python to PATH"

**"ModuleNotFoundError"**
- Run again: `pip install groq google-auth-oauthlib google-auth-httplib2 google-api-python-client`

**"client_secret file not found"**
- Make sure your `client_secret_*.json` file is in the ApplicationHelper folder

**OAuth not working**
- Run manually once: `python main.py`
- A browser should open for authorization
- If it doesn't, copy the URL from the terminal and paste in your browser

**Still having issues?**
- Make sure ALL 7 files are in the ApplicationHelper folder
- Check that folder path has no spaces or special characters
- Try running in Administrator mode (right-click run_app.bat → "Run as administrator")

---

## File Checklist

Before sending to Windows, verify you have:
- ✅ main.py
- ✅ llm.py
- ✅ config.py (with correct API keys!)
- ✅ resume.txt
- ✅ client_secret_*.json
- ✅ run_app.bat
- ✅ README.md

Missing any? Go back and add them before creating the zip!
