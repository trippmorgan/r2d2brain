"""
R2D2 Brain Configuration
Loads settings from environment variables or a .env file.
"""
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, rely on environment variables

# AI Backend: "gemini" or "ollama"
AI_BACKEND = os.getenv("AI_BACKEND", "ollama")

# Google Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Ollama (local models)
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://100.101.184.20:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral-small:24b")

# R2-D2 Hardware
R2_UUID = os.getenv("R2_UUID", "25B16450-58FD-1AC7-D75F-D9F2B6969811")
