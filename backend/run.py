"""
Simple run script - Execute from backend directory
Usage: python run.py
"""
import subprocess
import sys
import os

# Use active Python or venv Python
def get_python_exe():
    # If already running in a venv, use that
    if hasattr(sys, 'real_prefix') or (sys.base_prefix != sys.prefix):
        return sys.executable
    
    # Otherwise check for .venv
    venv_python = os.path.join(os.path.dirname(__file__), ".venv", "Scripts", "python.exe")
    if os.path.exists(venv_python):
        return venv_python
    
    # Fallback to current sys.executable
    return sys.executable

venv_python = get_python_exe()

print("🚀 Starting Pothole Detection Backend...")
print("📍 Server will be at: http://localhost:8000")
print("📖 API Docs at: http://localhost:8000/docs\n")
print(f"🐍 Using Python: {venv_python}")

# Run uvicorn using detected Python
subprocess.run([
    venv_python, "-m", "uvicorn",
    "app.main:app",
    "--host", "0.0.0.0",
    "--port", "8000",
    "--reload"
])
