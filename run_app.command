#!/bin/bash
# Application Helper Launcher for macOS
# Double-click this file to run the app
# Works from anywhere (desktop, downloads, etc.)

cd /Users/maxnguyen/ApplicationHelper || exit

# Run app in background
python3 main.py &
APP_PID=$!
sleep 1

# Minimize the Terminal window to dock
osascript -e 'tell application "Terminal" to set miniaturized of front window to true' 2>/dev/null

# Wait for app to close, then close terminal
wait $APP_PID
osascript -e 'tell application "Terminal" to close (get front window)' 2>/dev/null || true
