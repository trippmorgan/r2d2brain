# R2D2 Brain 🛰️🤖

AI-powered brain for the Sphero R2-D2, with voice control, sensor integration, autonomous exploration, and collision detection.

## Features

- **AI Agent** — Gemini or local Ollama models control R2's physical actions via structured JSON, with live sensor context
- **Autonomous Explorer** — R2 roams freely, avoids obstacles via collision detection, logs all sensor data, generates exploration reports
- **Sensor Monitor** — Real-time diagnostic display of accelerometer, gyroscope, locator, velocity, and orientation
- **Voice Control** — Speech recognition for hands-free interaction
- **Text Control** — Terminal-based command interface
- **Collision Detection** — Active across all modes; R2 reacts to impacts with sounds and evasive maneuvers
- **Sensor Logging** — All sensor data streamed to JSONL for analysis

## Quick Start

```bash
git clone https://github.com/trippmorgan/r2d2brain.git
cd r2d2brain

# Install dependencies
pip install -r requirements.txt

# Copy and edit config
cp .env.example .env
# Edit .env with your API keys and settings

# Run
python run.py
```

## Modes

### 1. AI Agent (Voice/Text + Sensors)
Full AI-powered control. R2 receives your commands via voice or text, and the AI sees R2's live sensor state (position, heading, speed, collisions) when making decisions.

### 2. Explorer (Autonomous Roaming)
R2 deploys tripod legs and roams autonomously:
- Rolls forward at random speeds/headings
- Detects collisions → backs up, turns away, continues
- Detects freefall/landing events
- Logs all sensor data to `/tmp/r2_sensor_log.jsonl`
- Generates exploration report to `/tmp/r2_exploration_report.md`
- Runs for configurable duration (default 60s) or until Ctrl+C

### 3. Sensor Monitor (Diagnostics)
Real-time terminal display of all sensor streams:
```
[12:30:01.234] ACCEL x=+0.02 y=-0.01 z=+1.00 | GYRO x=+0.5 y=-0.3 z=+0.1 | LOC x=0 y=0 | YAW=45
```
Also logs to JSONL file. Useful for calibration and debugging.

### 4. Brain (Manual Control)
Direct command matching with voice/text/autonomous modes. Now with collision detection — R2 reacts to impacts automatically.

## Architecture

```
User Input (voice/text) → AI Backend (Gemini/Ollama) → JSON Response → Robot Action
                                    ↑
                          [SENSOR STATE] injected
                          Position, heading, speed,
                          collisions, orientation
```

## Sensors Available

| Sensor | Data | Method |
|--------|------|--------|
| Accelerometer | x, y, z (g's) | `get_acceleration()` |
| Gyroscope | x, y, z (deg/s) | `get_gyroscope()` |
| Locator | x, y (relative) | `get_location()` |
| Velocity | x, y | `get_velocity()` |
| Orientation | pitch, roll, yaw | `get_orientation()` |
| Collision | event-based | `EventType.on_collision` |
| Freefall | event-based | `EventType.on_freefall` |
| Landing | event-based | `EventType.on_landing` |
| Gyro Max | event-based | `EventType.on_gyro_max` |

## Files

| File | Description |
|------|-------------|
| `run.py` | Entry point — mode selection menu |
| `r2_agent.py` | AI agent with sensor context integration |
| `r2_explorer.py` | Autonomous explorer with collision avoidance and reporting |
| `r2_sensors.py` | Real-time sensor monitor and diagnostic tool |
| `brain.py` | Standalone controller with collision detection |
| `config.py` | Configuration loader (env vars / `.env` file) |
| `ble_controller.py` | BLE control layer using `bleak` |
| `utils.py` | Low-level packet builder for BLE commands |

## Configuration

Copy `.env.example` to `.env` and edit:

```bash
# AI Backend: "gemini" or "ollama"
AI_BACKEND=ollama

# Google Gemini API Key (required if AI_BACKEND=gemini)
GOOGLE_API_KEY=your-key-here

# Ollama settings
OLLAMA_URL=http://100.101.184.20:11434
OLLAMA_MODEL=mistral-small:24b

# R2-D2 Bluetooth UUID
R2_UUID=25B16450-58FD-1AC7-D75F-D9F2B6969811

# Sensor & Exploration
SENSOR_LOG_PATH=/tmp/r2_sensor_log.jsonl
EXPLORATION_DURATION=60
EXPLORATION_SPEED=50
SENSOR_POLL_RATE=0.2
REPORT_PATH=/tmp/r2_exploration_report.md
```

## Hardware

- **Sphero R2-D2** (Bluetooth LE)
- **Sensors:** Accelerometer, gyroscope, locator, velocity, orientation, collision, freefall
- **No:** Camera, microphone, distance sensors
- **Microphone** (optional, for voice mode)
