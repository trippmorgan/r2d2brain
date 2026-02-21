# R2-D2 Vision Upgrade Guide 🔭

## Overview
Add a WiFi camera + microphone to the Sphero R2-D2 using a Seeed XIAO ESP32S3 Sense board.
No modification to R2's internal electronics — the camera is an independent system that rides along.

## Parts List

| # | Part | Price | Link |
|---|------|-------|------|
| 1 | **Seeed XIAO ESP32S3 Sense** (camera + mic included) | $13.99 | [Amazon](https://www.amazon.com/Seeed-Studio-XIAO-ESP32-Sense/dp/B0C69FFVHH) |
| 2 | **3.7V 100-150mAh LiPo battery** (JST 1.25mm connector) | $7.99 | [Amazon - 2 pack](https://www.amazon.com/dp/B08T6GT7DV) |
| 3 | **30AWG silicone wire** (for optional power tap) | $6.99 | [Amazon](https://www.amazon.com/dp/B07G2GLKMP) |
| 4 | **Kapton tape** (heat-resistant, for insulating solder joints) | $5.99 | [Amazon](https://www.amazon.com/dp/B07RZYY2SF) |
| | **Total** | **~$25-35** | |

### Optional but nice:
| Part | Price | Why |
|------|-------|-----|
| OV5640 camera module (upgrade) | $5 | Higher res (5MP vs 2MP), same ribbon connector |
| Micro SD card (any size) | $5 | Local recording / buffer |
| Helping hands / PCB holder | $10 | Makes soldering easier |

## Board Specs — XIAO ESP32S3 Sense

```
Dimensions:  21 x 17.5 x 7mm (smaller than a US quarter!)
CPU:         Dual-core Xtensa LX7 @ 240MHz
WiFi:        2.4GHz 802.11 b/g/n
BLE:         5.0
Camera:      OV2640 (1600x1200) on detachable flex ribbon
Microphone:  PDM digital mic (built-in!)
Memory:      8MB PSRAM + 8MB Flash
Storage:     MicroSD card slot
Power:       3.3V, ~150mA active streaming
Battery:     Built-in LiPo charging circuit (JST 1.25mm)
USB:         Type-C (for programming + charging)
GPIO:        11 pins (SPI, I2C, UART available)
```

## R2-D2 Internals Reference

```
R2's Dome (~55mm diameter):
┌─────────────────────────────────────┐
│           Dome Cover                │
│  ┌──────────────────────────────┐   │
│  │   3x LED boards (lights)    │   │
│  │                              │   │
│  │   Inner "Skull" piece        │   │
│  │                              │   │
│  │   Dome gearbox + servo       │   │
│  │   Potentiometer (feedback)   │   │
│  └──────────────────────────────┘   │
│                                     │
│   Body (below dome):               │
│   ┌─────────────────────────────┐   │
│   │ Board 1: STM32F (Cortex-M4)│   │
│   │   + 2x TI motor drivers    │   │
│   │                             │   │
│   │ Board 2: Nordic nRF51822    │   │
│   │   + Audio amp + Winbond     │   │
│   │   + USB charging            │   │
│   │                             │   │
│   │ 250mAh LiPo battery        │   │
│   │ Speaker (behind front vents)│   │
│   └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

## Installation Options

### Option A: Dome Mount (Recommended — Camera Rotates With Head!)
**Pro:** Camera turns when R2 looks around. Most realistic.
**Con:** Tighter space, need to route power wires through the dome joint.

1. Remove dome cover (2 snap-fits, use plastic spudger)
2. Remove inner skull (3 screws)
3. Route OV2640 ribbon cable through R2's front "logic display" opening
   - The rectangular port on R2's front dome is the perfect camera window
   - Lens sits flush behind the opening
4. Mount XIAO board against inside of skull wall with double-sided foam tape
5. Connect LiPo battery (JST 1.25mm — plug directly into XIAO)
6. Tuck battery in remaining dome space
7. Reassemble skull + dome cover

```
   R2 Front View:
   ┌───────────────┐
   │   ○  [CAM]  ○ │  ← Camera lens behind the logic display port
   │   ┌───────┐   │
   │   │ LIGHT │   │
   │   └───────┘   │
   └───────────────┘
```

### Option B: Body Mount (Easier but fixed angle)
**Pro:** More space, easier install, no wire routing through dome joint.
**Con:** Camera doesn't rotate with head. Fixed forward view.

1. Remove one body panel (2 screws)
2. Mount XIAO + camera behind one of R2's front body vents
3. Use the horizontal slot vents as a camera window
4. Connect to R2's battery (solder to LiPo leads) OR use separate battery
5. Replace body panel

### Option C: External Mount (Quickest — no disassembly)
**Pro:** Zero risk, reversible, 5 minutes.
**Con:** Not as clean looking.

1. 3D print or tape a small bracket to R2's dome
2. Mount XIAO with camera facing forward
3. Run USB-C cable to a small power bank on R2's back
4. Ugly but functional for testing before committing to internal mount

## Power Options

### 1. Separate LiPo (Safest — Recommended for first install)
- Plug a 100-150mAh LiPo into XIAO's JST connector
- Independent from R2's power — won't affect R2's battery life
- Charge XIAO via USB-C independently
- Runtime: ~45 min streaming at 150mAh

### 2. Tap R2's Battery (Advanced — more permanent)
- R2 has a 250mAh 3.7V LiPo
- Solder 30AWG wires to R2's battery leads (VCC + GND)
- Connect to XIAO's battery pads (BAT+ and BAT-)
- **Warning:** This cuts R2's already-short battery life roughly in half
- **Warning:** Only do this if you're confident in your solder skills
- Insulate all joints with Kapton tape

### 3. USB Power (Dev/Testing only)
- Run a thin USB-C cable out of R2's body to a power source
- Good for bench testing, bad for driving around

## Firmware — Flash the XIAO

### Install Arduino IDE + Board Support
```bash
# Arduino IDE: https://www.arduino.cc/en/software
# Or use PlatformIO in VS Code

# In Arduino IDE:
# File → Preferences → Additional Board URLs:
# https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
# Tools → Board → Boards Manager → Search "esp32" → Install
# Select board: "XIAO_ESP32S3"
```

### Camera Streaming Firmware
Save this as `r2_camera.ino` and flash via USB-C:

```cpp
#include "esp_camera.h"
#include <WiFi.h>

// ===== CONFIGURE YOUR WIFI =====
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// XIAO ESP32S3 Sense Camera Pin Map
#define PWDN_GPIO_NUM  -1
#define RESET_GPIO_NUM -1
#define XCLK_GPIO_NUM  10
#define SIOD_GPIO_NUM  40
#define SIOC_GPIO_NUM  39
#define Y9_GPIO_NUM    48
#define Y8_GPIO_NUM    11
#define Y7_GPIO_NUM    12
#define Y6_GPIO_NUM    14
#define Y5_GPIO_NUM    16
#define Y4_GPIO_NUM    18
#define Y3_GPIO_NUM    17
#define Y2_GPIO_NUM    15
#define VSYNC_GPIO_NUM 38
#define HREF_GPIO_NUM  47
#define PCLK_GPIO_NUM  13

WiFiServer server(80);

void setup() {
  Serial.begin(115200);

  // Camera config
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.frame_size = FRAMESIZE_VGA;  // 640x480
  config.jpeg_quality = 12;
  config.fb_count = 2;
  config.fb_location = CAMERA_FB_IN_PSRAM;

  // Init camera
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed: 0x%x\n", err);
    return;
  }

  // Connect WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected!");
  Serial.print("R2-CAM URL: http://");
  Serial.println(WiFi.localIP());

  server.begin();
}

void loop() {
  WiFiClient client = server.available();
  if (!client) return;

  String request = client.readStringUntil('\r');
  client.flush();

  if (request.indexOf("/capture") != -1) {
    // Single frame capture
    camera_fb_t* fb = esp_camera_fb_get();
    if (!fb) {
      client.println("HTTP/1.1 500 Internal Server Error");
      return;
    }
    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: image/jpeg");
    client.printf("Content-Length: %d\r\n", fb->len);
    client.println("Access-Control-Allow-Origin: *");
    client.println();
    client.write(fb->buf, fb->len);
    esp_camera_fb_return(fb);

  } else if (request.indexOf("/stream") != -1) {
    // MJPEG stream
    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: multipart/x-mixed-replace; boundary=frame");
    client.println();

    while (client.connected()) {
      camera_fb_t* fb = esp_camera_fb_get();
      if (!fb) break;
      client.printf("--frame\r\nContent-Type: image/jpeg\r\nContent-Length: %d\r\n\r\n", fb->len);
      client.write(fb->buf, fb->len);
      client.println();
      esp_camera_fb_return(fb);
    }

  } else {
    // Status page
    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: text/html");
    client.println();
    client.println("<h1>R2-D2 Camera Online</h1>");
    client.println("<p><a href='/capture'>Single Frame</a></p>");
    client.println("<p><a href='/stream'>MJPEG Stream</a></p>");
    client.printf("<p>Free heap: %d bytes</p>", ESP.getFreeHeap());
  }
  client.stop();
}
```

### Endpoints (once flashed and connected to WiFi):
- `http://<R2-CAM-IP>/` — Status page
- `http://<R2-CAM-IP>/capture` — Single JPEG frame
- `http://<R2-CAM-IP>/stream` — Live MJPEG stream

## Wiring the Vision to R2's Brain

### Update r2d2brain config (.env):
```bash
R2_CAMERA_URL=http://<R2-CAM-IP>
VISION_INTERVAL=2.0  # seconds between vision checks
VISION_MODEL=mistral-small:24b  # or qwen2.5:72b-instruct-q4_K_M for better analysis
```

### Vision capture in Python (add to r2_agent.py):
```python
import requests
from io import BytesIO
import base64

def capture_frame(camera_url):
    """Grab a single JPEG frame from R2's camera"""
    try:
        resp = requests.get(f"{camera_url}/capture", timeout=3)
        if resp.status_code == 200:
            return base64.b64encode(resp.content).decode('utf-8')
    except Exception as e:
        print(f"Camera error: {e}")
    return None

def describe_scene(frame_b64, ollama_url, model):
    """Send frame to Voldemort for description"""
    resp = requests.post(f"{ollama_url}/v1/chat/completions", json={
        "model": model,
        "messages": [
            {"role": "system", "content": "Describe what you see in this image in one short sentence. Focus on people, objects, and movement."},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{frame_b64}"}}
            ]}
        ],
        "max_tokens": 100
    })
    return resp.json()["choices"][0]["message"]["content"]
```

### Full vision loop integration:
```python
# In the AI agent main loop, before each AI query:
frame = capture_frame(R2_CAMERA_URL)
if frame:
    scene = describe_scene(frame, OLLAMA_URL, VISION_MODEL)
    sensor_context += f"\n[VISION] I see: {scene}"
# Now the AI knows what R2 sees + feels
```

## Assembly Checklist

- [ ] Order XIAO ESP32S3 Sense (~$14, Amazon Prime)
- [ ] Order small LiPo battery (~$8, Amazon Prime)
- [ ] Flash camera firmware via USB-C
- [ ] Test camera stream on bench (confirm WiFi + MJPEG works)
- [ ] Open R2's dome (2 snap-fits)
- [ ] Route camera ribbon to front logic display
- [ ] Mount XIAO board inside dome
- [ ] Connect LiPo battery
- [ ] Reassemble dome
- [ ] Update .env with camera IP
- [ ] Test full loop: Camera → Voldemort → AI → R2 reacts

## Expected Behavior After Upgrade

R2 will be able to:
- **See people** — react differently to someone approaching vs. leaving
- **Recognize objects** — excited about Star Wars memorabilia, scared of cats
- **Navigate better** — visual collision avoidance (supplement accelerometer)
- **Hear sounds** — microphone picks up voices, claps, etc.
- **Respond to visual commands** — hold up hand = stop, wave = come here
- **Autonomous personality** — wanders, looks around, comments on what it sees

## Timeline
- Day 1: Order parts (Amazon Prime = 1-2 day delivery)
- Day 2: Flash firmware, bench test camera streaming
- Day 3: Install in R2, solder if needed, test full integration
- Day 4: Tune AI prompts, adjust vision interval, enjoy your seeing R2 🤖
