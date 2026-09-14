"""LLM integration module using Groq for fast inference"""

from groq import Groq
from config import CONFIG


def initialize_groq():
    """Initialize Groq API with configured key"""
    api_key = CONFIG.get("groq_api_key")
    if not api_key or api_key == "gsk_":
        raise ValueError(
            "Groq API key not configured. Get a free key at https://console.groq.com/keys"
        )
    return Groq(api_key=api_key)


GROQ_MODEL = "qwen/qwen3.8-27b"  # Fast and reliable for text generation


def extract_ats_keywords(job_description: str) -> list:
    """
    Extract top 10 ATS keywords/phrases from job description using Groq (fast)
    
    Args:
        job_description: Full job description text
        
    Returns:
        List of top 10 ATS keywords/phrases
    """
    try:
        client = initialize_groq()
        
        # Simplified prompt for faster response
        prompt = f"""Analyze this job description and extract the top 10 most important keywords/phrases for ATS screening (technical skills, tools, years of experience, certifications).

Return ONLY a Python list, nothing else. Example: ["Python", "AWS", "5+ years", "Docker", "Kubernetes", "REST API", "PostgreSQL", "CI/CD", "Linux", "Agile"]

Job Description:
{job_description}

Keywords:"""
        
        message = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=200,
        )
        
        # Parse response as Python list
        import ast
        response_text = message.choices[0].message.content.strip()
        
        # Try to extract list from response
        keywords = ast.literal_eval(response_text)
        
        # Ensure it's a list of strings
        if isinstance(keywords, list):
            keywords = [str(k).strip() for k in keywords]
            # Debug: print to terminal
            print(f"✓ ATS Keywords extracted: {keywords}")
            return keywords[:10]
        
        return []
        
    except Exception as e:
        print(f"Error extracting ATS keywords: {str(e)}")
        return []


def generate_answer(question: str, job_description: str, ats_keywords: list, resume_text: str = "") -> str:
    """
    Generate an answer to an application question using Groq (fast)
    
    Args:
        question: The application question to answer
        job_description: The job description
        ats_keywords: List of ATS keywords to incorporate
        resume_text: User's resume text (optional)
        
    Returns:
        AI-generated answer to the question
    """
    try:
        client = initialize_groq()
        
        keywords_str = ", ".join(ats_keywords[:5]) if ats_keywords else ""
        resume_section = resume_text if resume_text else "No resume provided"
        
        prompt = f"""You're helping someone answer a job application question. Write a confident, friendly answer that sounds like a real person - someone who knows their stuff.

Resume (reference this for specific projects and skills):
{resume_section}

Job keywords they're looking for: {keywords_str}

The Question: {question}

Write the answer:
- 3+ sentences, natural and conversational (not corporate or robotic)
- Speak with confidence about your actual experience and accomplishments
- Reference specific projects, results, and technologies from your resume
- Include actual impact figures (95%, 1M+ users, etc.) ONLY when they're directly relevant to the question - not randomly
- When describing work, either naturally include company names OR describe the work objectively - avoid using "your/our" to refer to company work (sounds unprofessional)
- Weave in the keywords naturally where they match your real background
- NO apologizing, hedging, or self-diminishing language
- NO "I'm eager to learn" or "while I haven't yet" - sound like you've got this
- No markdown, asterisks, or formatting
- Copy-paste ready

Answer:"""
        
        message = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=250,
        )
        
        return message.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"Error generating answer: {str(e)}")
        return "Error generating answer. Please try again."


def research_company(company_name: str, job_description: str) -> str:
    """
    Research company mission and what they do using Groq
    
    Args:
        company_name: Name of the company
        job_description: The job description for context
        
    Returns:
        Specific info about company mission and what they do
    """
    try:
        client = initialize_groq()
        
        prompt = f"""Based on the company name and job description, provide a 2-3 sentence summary about:
1. What this company does / their product or service
2. Their mission or what they're known for
3. Why this is relevant to the job role

Be specific and factual. This will be used for a personalized cover letter.

Company: {company_name}
Job Description: {job_description[:300]}

Summary:"""
        
        message = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=200,
        )
        
        return message.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"Error researching company: {str(e)}")
        return ""


def generate_cover_letter(job_description: str, company_name: str, ats_keywords: list, template: str = "", resume_text: str = "") -> str:
    """
    Generate a customized cover letter using Groq (fast) and save to Downloads
    
    Args:
        job_description: The job description
        company_name: Name of the company
        ats_keywords: List of ATS keywords to incorporate
        template: Optional cover letter template to follow
        resume_text: User's resume text (optional)
        
    Returns:
        Path to saved cover letter file
    """
    try:
        client = initialize_groq()
        
        # Research the company first
        company_info = research_company(company_name, job_description)
        
        keywords_str = ", ".join(ats_keywords[:8]) if ats_keywords else ""
        resume_section = resume_text if resume_text else ""
        
        prompt = f"""Write a professional cover letter that sounds like a real person - direct, confident, and human. NOT flowery or AI-sounding.

Company Info (use this to personalize):
Name: {company_name}
Mission/What they do: {company_info}

Candidate's Background (use ONLY what's here, nothing made up):
{resume_section}

Job Requirements: {job_description}

Key skills they want: {keywords_str}

Write the cover letter with this exact structure:

PARAGRAPH 1 - Opening (personalized to this company):
- Start with today's date (format: Month D, YYYY)
- Then company name and "Dear Hiring Manager,"
- Open with genuine interest in the role
- Include a line like: "I'm excited to work at {company_name} because [specific reason based on their mission/what they do]"
- Show you understand what they do and why it matters
- Keep it direct and conversational

PARAGRAPH 2 - Your Experience:
- Reference actual companies (Haptic Vision, Mozilla, Athletic Testing) by name
- Include specific achievements with metrics when relevant (95% latency, 1M+ users, etc.)
- Connect these achievements to what {company_name} needs
- Show you can handle their challenges

PARAGRAPH 3 - One Concrete Example:
- Pick the most relevant project from your background
- Include results and metrics
- Explain why this matters for the role
- Sound confident about your capability

PARAGRAPH 4 - Closing:
- Express genuine interest and readiness
- Invite conversation
- No apologizing or hedging
- End with blank line, then "Best regards," then blank line, then "Andrew Nguyen"

General requirements:
- Sound like a smart, direct person (not AI prose or flowery language)
- Include metrics ONLY when they directly support your point
- NO markdown, NO asterisks
- About 300 words total
- Copy-paste ready

Write it:"""
        
        message = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=1200,
        )
        
        cover_letter_text = message.choices[0].message.content.strip()
        
        # Save to Downloads folder with simple naming
        import os
        
        downloads_path = os.path.expanduser("~/Downloads")
        filename = f"Andrew Nguyen Cover Letter - {company_name}.txt"
        filepath = os.path.join(downloads_path, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cover_letter_text)
        
        print(f"✓ Cover letter saved to {filepath}")
        return filepath
        
    except Exception as e:
        print(f"Error generating cover letter: {str(e)}")
        return None


def list_google_sheets_worksheets() -> list:
    """
    List all worksheets in the Google Sheet to help with debugging
    
    Returns:
        List of worksheet names
    """
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        import os
        
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        
        creds = None
        token_path = os.path.expanduser("~/.application_helper_token.json")
        credentials_path = os.path.expanduser("~/ApplicationHelper/client_secret_529921471730-91v6i14inb2jdidqg622fmk8hgloffai.apps.googleusercontent.com.json")
        
        # Load existing token
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            elif os.path.exists(credentials_path):
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
                with open(token_path, 'w') as token_file:
                    token_file.write(creds.to_json())
        
        # Get spreadsheet info
        service = build('sheets', 'v4', credentials=creds)
        sheet_id = CONFIG.get("google_sheets_id")
        
        spreadsheet = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
        sheets = spreadsheet.get('sheets', [])
        
        sheet_names = []
        for sheet in sheets:
            sheet_names.append(sheet['properties']['title'])
        
        return sheet_names
        
    except Exception as e:
        print(f"Error listing worksheets: {e}")
        return []


def append_to_google_sheets(job_link: str, company_name: str) -> bool:
    """
    Append application record to Google Sheets
    
    Args:
        job_link: Link to the job posting
        company_name: Name of the company
        
    Returns:
        True if successful, False otherwise
    """
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        from datetime import datetime
        import os
        import json
        
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        
        creds = None
        token_path = os.path.expanduser("~/.application_helper_token.json")
        credentials_path = os.path.expanduser("~/ApplicationHelper/client_secret_529921471730-91v6i14inb2jdidqg622fmk8hgloffai.apps.googleusercontent.com.json")
        
        # Load existing token if available
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        
        # If no valid credentials, create new auth flow
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            elif os.path.exists(credentials_path):
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
                
                # Save credentials for next time
                with open(token_path, 'w') as token_file:
                    token_file.write(creds.to_json())
            else:
                print(f"Error: Credentials file not found: {credentials_path}")
                return False
        
        # Build Sheets API client
        service = build('sheets', 'v4', credentials=creds)
        
        # Get sheet info
        sheet_id = CONFIG.get("google_sheets_id")
        sheet_name = CONFIG.get("google_sheets_name", "Internships")
        
        # Prepare data to append (job link + "Applied" status)
        values = [[job_link, "Applied"]]
        
        # Append to sheet
        body = {'values': values}
        result = service.spreadsheets().values().append(
            spreadsheetId=sheet_id,
            range=f"{sheet_name}!A:B",
            valueInputOption='USER_ENTERED',
            body=body
        ).execute()
        
        print(f"✓ Application logged to Google Sheets")
        return True
        
    except Exception as e:
        print(f"Error syncing to Google Sheets: {str(e)}")
        print("Your application is still being tracked locally.")
        return False
