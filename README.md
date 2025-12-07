
# R2D2 Brain
pip install google-generativeai
This project powers an AI-enhanced robotic brain for the Sphero R2D2 toy using Python and vision/audio inputs.
pip install spherov2
## Features
- Voice command interface
- Camera-based object detection
- WebSocket control interface
npm install @abandonware/noble
## Getting Started
```bash
git clone https://github.com/trippmorgan/r2d2brain.git
cd r2d2brain
conda activate myenv && pip install bleak
pip install -r requirements.txt
python run.py
pip install "numpy<2.0,>=1.23.5"
# R2D2Brain 🛰️🤖
pip install spherov2
Interactive R2-D2 Controller powered by voice, vision, and Bluetooth Low Energy (BLE)!
python -m r2d2brain.run

Connects to R2D2 via BLE and lets you interact using speech and camera vision.
To run these scripts, you'll need to:
1. Install Dependencies
pip install spherov2 bleak
For the keyboard control script, you'll also need:
pip install keyboard
2. Run a Script
Make sure your R2D2 is powered on and Bluetooth is enabled on your Mac, then:
# Basic connection test
python3 hellor2d2.py

# Collision detection demo
python3 animatetestr2.py

# Keyboard control (requires sudo for keyboard access)
sudo python3 keyboardr2d2.py
3. For the AI Brain (r2d2brain)
This requires more setup:
cd r2d2brain
pip install -r requirements.txt
python3 run.py
Note: The brain module needs:
A microphone for voice commands
The Qwen2VL model downloaded to a ./models folder
Your specific R2D2's Bluetooth address (currently hardcoded in brain.py)
Troubleshooting
"No Sphero toy found" - Make sure R2D2 is on and not connected to another device
Bluetooth permission errors - On macOS, grant Terminal/your IDE Bluetooth access in System Preferences → Privacy & Security → Bluetooth
keyboard module errors - Must run with sudo on macOS
Would you like me to help with any specific script or setup issue?