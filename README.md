# R2D2Brain 🤖🛰️

An interactive AI-powered controller for the Sphero R2-D2 toy that brings the beloved droid to life using voice commands, computer vision, and Bluetooth Low Energy (BLE) communication.

## 🌟 Features

- **Voice Control**: Speak naturally to R2-D2 using Google Speech Recognition
- **Vision Processing**: AI-powered object detection using Qwen2-VL model
- **BLE Communication**: Direct wireless control via Bluetooth Low Energy
- **Real-time Response**: Asynchronous processing for smooth interaction

## 📋 Prerequisites

### Hardware
- Sphero R2-D2 toy robot
- Computer with Bluetooth 4.0+ (BLE support)
- Microphone for voice input
- (Optional) Camera for vision features

### Software
- **Python 3.8+** (tested on 3.8-3.11)
- **Operating System**: Linux, macOS, or Windows with BLE support
- **PortAudio** (required for microphone access)

## 🚀 Installation

### 1. System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install python3-dev portaudio19-dev libasound2-dev
```

**macOS:**
```bash
brew install portaudio
```

**Windows:**
- Install [PyAudio wheel](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) manually
- Ensure Bluetooth drivers are installed

### 2. Clone Repository

```bash
git clone https://github.com/trippmorgan/r2d2brain.git
cd r2d2brain
```

### 3. Install Python Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 4. Download Vision Model (Optional)

If using vision features, download the Qwen2-VL model:

```bash
mkdir -p models
# Download model files to ./models directory
# See: https://huggingface.co/Qwen/Qwen2-VL
```

## ⚙️ Configuration

### Find Your R2-D2's BLE Address

**Linux:**
```bash
bluetoothctl
scan on
# Look for "R2-D2" or similar device
# Note the MAC address (format: XX:XX:XX:XX:XX:XX)
```

**macOS:**
- Open System Preferences → Bluetooth
- Note the device address when R2-D2 appears

**Windows:**
- Use Device Manager → Bluetooth
- Right-click R2-D2 device → Properties → Details

### Update Configuration

Edit `brain.py` line 9 and replace the placeholder address:

```python
r2d2 = R2D2Controller(address="YOUR:R2:D2:MAC:ADDRESS")
```

Example:
```python
r2d2 = R2D2Controller(address="A1:B2:C3:D4:E5:F6")
```

## 🎮 Usage

### Basic Start

```bash
# Activate virtual environment if you created one
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the application
python run.py
```

### Expected Output

```
Loading vision model...
Connecting to R2-D2...
Connected to R2D2
Listening for voice commands...
```

### Voice Commands

Speak clearly into your microphone. The system will:
1. Listen for your voice
2. Convert speech to text using Google Speech Recognition
3. Display recognized text
4. Process commands to control R2-D2

## 📁 Project Structure

```
r2d2brain/
├── __init__.py           # Package initialization
├── brain.py              # Main controller logic
├── ble_controller.py     # Bluetooth Low Energy interface
├── voice.py              # Speech recognition setup
├── vision.py             # Computer vision model loader
├── utils.py              # Helper functions (packet building)
├── run.py                # Application entry point
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🔧 Troubleshooting

### Bluetooth Connection Issues

**Problem**: "Failed to connect to R2-D2"
- **Solution**:
  - Ensure R2-D2 is powered on and in pairing mode
  - Verify the MAC address is correct in `brain.py`
  - Try running with `sudo` on Linux (if permission denied)
  - Disconnect other devices connected to R2-D2

### Microphone Not Working

**Problem**: "No microphone found" or "Recognition error"
- **Solution**:
  - Check microphone permissions on your OS
  - Test microphone with other applications
  - Verify PortAudio installation: `pip show pyaudio`
  - On Linux, add user to `audio` group: `sudo usermod -a -G audio $USER`

### Import Errors

**Problem**: `ModuleNotFoundError` or import errors
- **Solution**:
  - Ensure virtual environment is activated
  - Reinstall dependencies: `pip install -r requirements.txt --upgrade`
  - Check Python version: `python --version` (should be 3.8+)

### Vision Model Issues

**Problem**: Model fails to load
- **Solution**:
  - Verify model files are in `./models` directory
  - Check available disk space and RAM
  - For CPU-only systems, ensure PyTorch CPU version is installed
  - Comment out vision features if not needed

## 🛠️ Development

### Running in Development Mode

```bash
# Install development dependencies
pip install -e .

# Run with debug output
python -m r2d2brain.run
```

### Code Style

This project follows PEP 8 guidelines. Format code with:
```bash
pip install black
black .
```

## 📝 Dependencies

Core dependencies (see `requirements.txt`):
- `bleak` - BLE communication
- `torch` - Deep learning framework
- `transformers` - AI model loading (Qwen2-VL)
- `speechrecognition` - Voice recognition
- `pyaudio` - Microphone access
- `opencv-python` - Computer vision
- `Pillow` - Image processing

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source. Please check with Sphero regarding their API usage policies.

## 🙏 Acknowledgments

- Sphero for creating the amazing R2-D2 robot
- Google Speech Recognition API
- Qwen2-VL vision model team
- Open source community

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Provide error logs and system information

---

**Note**: This is an unofficial project and is not affiliated with Sphero or Lucasfilm.

May the Force be with you! 🌌
