#!/usr/bin/env python3
"""
Build script to create standalone executables for macOS and Windows
Run: python3 build_app.py
"""

import subprocess
import sys
import os

def build_app():
    """Build the application using PyInstaller"""
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Get the directory where this script is located
    app_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("\n" + "="*70)
    print("Building Application Helper as standalone executable...")
    print("="*70 + "\n")
    
    # PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", "Application Helper",
        "--onefile",  # Single executable file
        "--windowed",  # No console window
        "--icon", "app_icon.icns" if sys.platform == "darwin" else None,  # macOS icon
        "--add-data", f"{app_dir}/config.py:.",
        "--add-data", f"{app_dir}/llm.py:.",
        "--add-data", f"{app_dir}/resume.txt:.",
        "--add-data", f"{app_dir}/client_secret_*.json:.",
        "--hidden-import", "google.auth",
        "--hidden-import", "google.oauth2",
        "--hidden-import", "google_auth_oauthlib",
        "--hidden-import", "googleapiclient",
        "--hidden-import", "groq",
        f"{app_dir}/main.py"
    ]
    
    # Remove None values
    cmd = [c for c in cmd if c is not None]
    
    try:
        subprocess.check_call(cmd)
        print("\n" + "="*70)
        print("✅ Build successful!")
        print("="*70)
        
        if sys.platform == "darwin":
            print("\n📱 macOS: Look in 'dist/' folder for 'Application Helper.app'")
            print("   You can drag it to Applications folder")
        elif sys.platform == "win32":
            print("\n💻 Windows: Look in 'dist/' folder for 'Application Helper.exe'")
            print("   You can create a shortcut on your desktop")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_app()
