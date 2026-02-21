# R2D2 Brain 🛰️🤖

AI-powered brain for the Sphero R2-D2, with voice control, vision, and autonomous behavior.

## Features

- **AI Agent** — Gemini or local Ollama models control R2's physical actions via structured JSON
- **Voice Control** — Speech recognition for hands-free interaction
- **Text Control** — Terminal-based command interface
- **Autonomous Mode** — Random behavior with personality (via `brain.py`)
- **BLE Protocol** — Low-level Bluetooth control (Node.js reference in `r2_chirp.js`)
- **Vision** — Camera-based object detection (WIP)

## Quick Start

```bash
git clone https://github.com/trippmorgan/r2d2brain.git
cd r2d2brain

# Install dependencies
pip install -r requirements.txt

# Copy and edit config
cp .env.example .env
# Edit .env with your API keys and settings

# Run the AI agent
python run.py
```

## Architecture

The agent follows a simple loop:

```
User Input (voice/text) → AI Backend (Gemini/Ollama) → JSON Response → Robot Action
```

1. **Input** — Voice (speech recognition) or text (terminal)
2. **AI** — The backend receives the input plus a system prompt describing available actions
3. **JSON** — The AI responds with structured JSON containing a text response and an action
4. **Action** — The agent translates the JSON into physical R2-D2 commands (drive, animate, turn, etc.)

## Files

| File | Description |
|------|-------------|
| `r2_agent.py` | Main AI agent — Gemini + Ollama backends, voice/text input |
| `brain.py` | Standalone controller — no AI, direct command matching with voice/text/autonomous modes |
| `config.py` | Configuration loader (env vars / `.env` file) |
| `vision.py` | Vision module — camera-based object detection (WIP) |
| `ble_controller.py` | BLE control layer using `bleak` |
| `utils.py` | Low-level packet builder for BLE commands |
| `r2_chirp.js` | Low-level BLE implementation (Node.js reference) |
| `run.py` | Entry point — runs the AI agent |
| `utils/r2_alive.py` | Hardware test — lights, sounds, animations, movement |
| `utils/r2_capabilities.py` | Dumps all available sounds and animations |
| `utils/r2_test_actions.py` | Tests robot actions via BLE controller |
| `utils/test_controller.py` | Tests controller methods |
| `utils/test_connection.py` | Basic BLE connection test |
| `utils/keyboard_r2.py` | WASD keyboard control |

## Configuration

Copy `.env.example` to `.env` and edit:

```bash
# AI Backend: "gemini" or "ollama"
AI_BACKEND=ollama

# Google Gemini API Key (required if AI_BACKEND=gemini)
GOOGLE_API_KEY=your-key-here

# Ollama settings (local model support)
OLLAMA_URL=http://100.101.184.20:11434
OLLAMA_MODEL=mistral-small:24b

# R2-D2 Bluetooth UUID
R2_UUID=25B16450-58FD-1AC7-D75F-D9F2B6969811
```

## Hardware

- **Sphero R2-D2** (Bluetooth LE)
- **Microphone** (for voice mode)
- **Camera** (for vision mode, optional)
