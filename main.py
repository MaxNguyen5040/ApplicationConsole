import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import pyperclip
from datetime import datetime
from queue import Queue
from config import CONFIG
from llm import extract_ats_keywords, generate_answer, generate_cover_letter, append_to_google_sheets


class JobApplicationHelper:
    def __init__(self, root):
        self.root = root
        self.root.title("Job Application Helper")
        self.root.geometry("1900x1100")
        
        # State management
        self.job_description = ""
        self.job_link = ""
        self.ats_keywords = []
        self.questions_answers = {}
        self.resume_text = self.load_resume()
        
        # Thread-safe queue for reset command
        self.reset_queue = Queue()
        
        # Setup UI
        self.setup_top_bar()
        self.setup_main_content()
        
        # Check queue periodically for reset command
        self.check_reset_queue()
        
        # Setup window close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_top_bar(self):
        """Create the fixed top bar with 4 copy buttons"""
        top_frame = ttk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=3, pady=3)
        
        buttons = [
            ("LinkedIn", "linkedin"),
            ("School", "school"),
            ("GitHub", "github"),
            ("Past Job", "past_job"),
        ]
        
        for button_text, config_key in buttons:
            btn = ttk.Button(
                top_frame,
                text=button_text,
                command=lambda key=config_key: self.copy_to_clipboard(key),
            )
            btn.pack(side=tk.LEFT, padx=2, pady=2, fill=tk.BOTH, expand=True)
    
    def copy_to_clipboard(self, config_key):
        """Copy configured data to clipboard"""
        try:
            data = CONFIG[config_key]
            pyperclip.copy(data)
            # Silent copy - no popup
        except Exception as e:
            pass  # Silent fail
    
    def load_resume(self):
        """Load resume from file"""
        try:
            resume_path = CONFIG.get("resume_path", "")
            if resume_path and __import__('os').path.exists(resume_path):
                with open(resume_path, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception as e:
            print(f"Error loading resume: {e}")
        return ""
    
    def setup_main_content(self):
        """Create the main content area with screens"""
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Screen 1: Job Description Input
        self.create_screen1()
    
    def create_screen1(self):
        """Screen 1: Paste job description"""
        self.clear_main_frame()
        
        label = ttk.Label(self.main_frame, text="Paste Job Description", font=("Arial", 14, "bold"))
        label.pack(pady=10)
        
        self.job_desc_text = scrolledtext.ScrolledText(
            self.main_frame,
            height=15,
            width=80,
            font=("Arial", 11)
        )
        self.job_desc_text.pack(fill=tk.BOTH, expand=True, pady=10)
        self.job_desc_text.bind("<KeyRelease>", self.on_job_description_change)
        
        # Focus on the text field
        self.job_desc_text.focus()
    
    def on_job_description_change(self, event):
        """Detect when job description text is entered"""
        content = self.job_desc_text.get("1.0", tk.END).strip()
        
        if content and not self.job_description:
            # First time content detected - show screen 2 and start ATS extraction
            self.job_description = content
            self.create_screen2()
            # Start ATS extraction in background
            self.extract_ats_background()
        elif content:
            # Update stored content
            self.job_description = content
    
    def create_screen2(self):
        """Screen 2: Paste job link only (job description hidden to save space)"""
        self.clear_main_frame()
        
        # Job link input
        label = ttk.Label(self.main_frame, text="Paste Job Link", font=("Arial", 14, "bold"))
        label.pack(pady=20)
        
        self.job_link_text = tk.Entry(
            self.main_frame,
            font=("Arial", 11),
            width=80
        )
        self.job_link_text.pack(fill=tk.X, padx=5, pady=5)
        self.job_link_text.bind("<KeyRelease>", self.on_job_link_change)
        
        # Focus on the job link field
        self.job_link_text.focus()
        
        # Status indicator for ATS extraction (placeholder for now)
        self.status_label = ttk.Label(
            self.main_frame,
            text="🔄 Extracting ATS keywords in background...",
            font=("Arial", 10)
        )
        self.status_label.pack(pady=10)
    
    def on_job_link_change(self, event):
        """Detect when job link is entered"""
        content = self.job_link_text.get().strip()
        
        if content and not self.job_link:
            # First time link detected - show screen 3
            self.job_link = content
            self.create_screen3()
        elif content:
            # Update stored link
            self.job_link = content
    
    def extract_ats_background(self):
        """Run ATS extraction in background thread"""
        def extraction_worker():
            try:
                keywords = extract_ats_keywords(self.job_description)
                self.ats_keywords = keywords
                # Update UI in main thread
                if hasattr(self, 'status_label'):
                    if keywords:
                        keywords_text = ", ".join(keywords)
                        status_text = f"✓ ATS Keywords: {keywords_text}"
                        self.status_label.config(text=status_text, foreground="green")
                    else:
                        self.status_label.config(text="✗ No keywords extracted", foreground="red")
            except Exception as e:
                print(f"ATS extraction failed: {e}")
                if hasattr(self, 'status_label'):
                    self.status_label.config(text="✗ ATS extraction failed", foreground="red")
        
        thread = threading.Thread(target=extraction_worker, daemon=True)
        thread.start()
    
    def create_screen3(self):
        """Screen 3: Question answerer chatbox"""
        self.clear_main_frame()
        
        # Summary section at top
        summary_frame = ttk.LabelFrame(self.main_frame, text="Job Application Summary", padding=10)
        summary_frame.pack(fill=tk.X, padx=5, pady=5)
        
        summary_text = f"""
Job Link: {self.job_link}
Job Description Length: {len(self.job_description)} characters
Status: Ready for questions
        """
        summary_label = ttk.Label(summary_frame, text=summary_text.strip(), font=("Arial", 9))
        summary_label.pack(anchor=tk.W)
        
        # Chatbox section
        chat_label = ttk.Label(self.main_frame, text="Answer Application Questions", font=("Arial", 14, "bold"))
        chat_label.pack(pady=10)
        
        self.question_text = scrolledtext.ScrolledText(
            self.main_frame,
            height=12,
            width=80,
            font=("Arial", 11)
        )
        self.question_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.question_text.bind("<KeyRelease>", self.on_question_change)
        
        # Answers display
        answer_label = ttk.Label(self.main_frame, text="AI-Generated Answers (click to copy)", font=("Arial", 12, "bold"))
        answer_label.pack(pady=(10, 0))
        
        self.answers_frame = ttk.Frame(self.main_frame)
        self.answers_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.answers_text = scrolledtext.ScrolledText(
            self.answers_frame,
            height=6,
            width=80,
            font=("Arial", 10),
            state=tk.DISABLED
        )
        self.answers_text.pack(fill=tk.BOTH, expand=True)
        self.setup_answer_click()
        
        # Button section
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=10)
        
        cover_letter_btn = ttk.Button(
            button_frame,
            text="Generate Cover Letter",
            command=self.generate_cover_letter
        )
        cover_letter_btn.pack(side=tk.LEFT, padx=5)
        
        submit_btn = ttk.Button(
            button_frame,
            text="Submit Application",
            command=self.submit_application
        )
        submit_btn.pack(side=tk.RIGHT, padx=5)
        
        # Focus on the question field
        self.question_text.focus()
    
    def on_question_change(self, event):
        """Handle question input - generate answer immediately on paste"""
        # Get current question
        question = self.question_text.get("1.0", tk.END).strip()
        
        if question:
            # Show loading state
            self.answers_text.config(state=tk.NORMAL)
            self.answers_text.delete("1.0", tk.END)
            self.answers_text.insert("1.0", "Generating answer...")
            self.answers_text.config(state=tk.DISABLED)
            
            # Generate answer immediately
            self.generate_and_display_answer(question)
        else:
            self.answers_text.config(state=tk.NORMAL)
            self.answers_text.delete("1.0", tk.END)
            self.answers_text.config(state=tk.DISABLED)
    
    def generate_and_display_answer(self, question):
        """Generate answer and display it in the UI"""
        def answer_worker():
            try:
                answer = generate_answer(
                    question=question,
                    job_description=self.job_description,
                    ats_keywords=self.ats_keywords,
                    resume_text=self.resume_text
                )
                
                # Update UI in main thread
                self.answers_text.config(state=tk.NORMAL)
                self.answers_text.delete("1.0", tk.END)
                self.answers_text.insert("1.0", answer)
                self.answers_text.config(state=tk.DISABLED)
            except Exception as e:
                print(f"Error generating answer: {e}")
        
        thread = threading.Thread(target=answer_worker, daemon=True)
        thread.start()
    
    def copy_answer(self):
        """Copy the current answer to clipboard when answer box is clicked"""
        answer = self.answers_text.get("1.0", tk.END).strip()
        if answer:
            pyperclip.copy(answer)
            # Silent copy - no popup
    
    def setup_answer_click(self):
        """Setup click binding for answer box to auto-copy"""
        self.answers_text.bind("<Button-1>", lambda e: self.copy_answer())
    
    def generate_cover_letter(self):
        """Generate and save cover letter to Downloads folder"""
        def cover_letter_worker():
            try:
                # Use "Company" as placeholder - you'll handle extraction separately
                filepath = generate_cover_letter(
                    job_description=self.job_description,
                    company_name="Company",
                    ats_keywords=self.ats_keywords,
                    resume_text=self.resume_text
                )
                
                if filepath:
                    print(f"✓ Cover letter saved")
            except Exception as e:
                print(f"Error generating cover letter: {e}")
        
        thread = threading.Thread(target=cover_letter_worker, daemon=True)
        thread.start()
    
    def submit_application(self):
        """Submit application, log to Google Sheets, and reset"""
        def submit_worker():
            try:
                # Log to Google Sheets
                if self.job_link:
                    append_to_google_sheets(self.job_link, "Application")
                else:
                    print("No job link provided")
                
                # Signal main thread to reset
                self.reset_queue.put("RESET")
            except Exception as e:
                print(f"Error submitting application: {e}")
        
        thread = threading.Thread(target=submit_worker, daemon=True)
        thread.start()
    
    def check_reset_queue(self):
        """Check if background thread requested a reset"""
        try:
            if not self.reset_queue.empty():
                command = self.reset_queue.get_nowait()
                if command == "RESET":
                    self.job_description = ""
                    self.job_link = ""
                    self.ats_keywords = []
                    self.questions_answers = {}
                    self.create_screen1()
        except:
            pass
        
        # Schedule next check
        self.root.after(100, self.check_reset_queue)
    
    def on_closing(self):
        """Handle window close - close the terminal too"""
        import subprocess
        import os
        
        # Close the terminal window on macOS
        try:
            subprocess.run([
                'osascript', '-e',
                'tell application "Terminal" to quit'
            ], timeout=1)
        except:
            pass
        
        # Close the app
        self.root.destroy()
    
    def reset_app(self):
        """Reset app to initial state"""
        self.job_description = ""
        self.job_link = ""
        self.ats_keywords = []
        self.questions_answers = {}
        self.create_screen1()
    
    def clear_main_frame(self):
        """Clear all widgets from main frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()


def main():
    root = tk.Tk()
    app = JobApplicationHelper(root)
    root.mainloop()


if __name__ == "__main__":
    main()
