# Configuration file for Application Helper
# Users can edit the .env file to customize the data copied by top bar buttons

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

CONFIG = {
    "linkedin": os.getenv("LINKEDIN_URL", "https://www.linkedin.com/in/your-profile/"),
    "school": os.getenv("SCHOOL", "Your School Name"),
    "github": os.getenv("GITHUB_URL", "https://github.com/your-username"),
    "past_job": os.getenv("PAST_JOB", "Your Company Name"),
    "groq_api_key": os.getenv("GROQ_API_KEY"),  # Get your FREE API key from https://console.groq.com/keys
    "resume_path": os.path.join(os.path.dirname(__file__), "resume.txt"),  # Path to your resume
    "google_sheets_id": os.getenv("GOOGLE_SHEETS_ID"),  # Your Google Sheet ID
    "google_sheets_name": os.getenv("GOOGLE_SHEETS_NAME", "Internships"),  # Worksheet name
}
