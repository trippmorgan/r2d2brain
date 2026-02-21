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

# Sensor & Exploration Settings
SENSOR_LOG_PATH = os.getenv("SENSOR_LOG_PATH", "/tmp/r2_sensor_log.jsonl")
EXPLORATION_DURATION = int(os.getenv("EXPLORATION_DURATION", "60"))
EXPLORATION_SPEED = int(os.getenv("EXPLORATION_SPEED", "50"))
SENSOR_POLL_RATE = float(os.getenv("SENSOR_POLL_RATE", "0.2"))
REPORT_PATH = os.getenv("REPORT_PATH", "/tmp/r2_exploration_report.md")
