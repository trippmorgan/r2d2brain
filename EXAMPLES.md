# R2D2 Brain - Use Examples and Expected Outcomes

This document provides practical examples of how to interact with your R2D2 using voice commands, vision recognition, and combined multimodal interactions.

---

## 🎤 Voice Command Examples

### Basic Movement Commands

#### **"Dance, R2!"**
**Expected Outcome:**
- R2D2 performs a choreographed dance routine
- Spins 360° clockwise
- Waddles side-to-side 3 times
- Rocks back and forth
- Plays excited beeping sounds
- Total duration: ~15 seconds

**Technical Details:**
- Combines rotation, roll, and stance animations
- LED dome lights flash in sync with movements
- Audio plays from internal speaker

---

#### **"Follow me"**
**Expected Outcome:**
- R2D2 activates vision tracking mode
- Camera continuously monitors for human detection
- Maintains 2-3 feet distance from detected person
- Adjusts speed based on person's movement
- Stops when person stops moving
- Exits mode after 30 seconds of no movement detected or voice command "stop following"

**Technical Details:**
- Uses vision model to detect and track person
- Calculates distance using bounding box size
- Adjusts heading to keep person centered in frame
- Speed varies: 0-50% of max speed

---

#### **"Spin around"**
**Expected Outcome:**
- R2D2 rotates 360° clockwise
- Rotation speed: moderate (2 seconds total)
- Dome LED lights up during spin
- Plays mechanical rotation sound

**Alternative Commands:**
- "Turn around"
- "Do a spin"
- "Rotate 360"

---

#### **"Move forward"**
**Expected Outcome:**
- R2D2 rolls forward for 2 seconds
- Speed: 30% of maximum
- Travels approximately 1-2 feet
- Head dome remains stationary

**Variations:**
- "Go forward" - same as above
- "Move backward" / "Go back" - reverses direction
- "Go left" / "Go right" - strafes in specified direction

---

#### **"Stop"**
**Expected Outcome:**
- Immediately halts all movement
- Plays acknowledgment beep
- Cancels any active movement commands or modes
- Resets to idle state

---

### Expressive Commands

#### **"Act scared"**
**Expected Outcome:**
- R2D2 quickly rolls backward 6 inches
- Head dome rotates rapidly left-right
- Plays worried beeping sounds (ascending pitch)
- LEDs flash red briefly
- Returns to cautious stance
- Duration: ~5 seconds

---

#### **"Be excited"**
**Expected Outcome:**
- Rapid waddle motion (shifting weight side-to-side)
- Head dome spins continuously
- Plays cheerful, rapid beeping sequence
- LED dome cycles through blue and white colors
- Small forward-backward rocking motions
- Duration: ~8 seconds

---

#### **"Look around"**
**Expected Outcome:**
- Head dome rotates 360° slowly
- Pauses briefly at 90° intervals
- Body remains stationary
- Plays soft scanning beeps at each pause
- Returns to forward-facing position
- Duration: ~10 seconds

---

#### **"Nod yes"**
**Expected Outcome:**
- R2D2 tilts forward and back 3 times
- Uses stance adjustment to simulate nodding
- Plays affirmative beep pattern
- Duration: ~3 seconds

**Alternative:** "Shake your head no" - waddles left-right instead

---

### Patrol and Navigation

#### **"Patrol the room"**
**Expected Outcome:**
- R2D2 begins autonomous navigation pattern
- Moves in expanding spiral pattern or wall-following behavior
- Vision system monitors for obstacles
- Automatically avoids detected obstacles
- Plays occasional scanning beeps
- Continues for 60 seconds or until "stop" command
- Reports "Patrol complete" with sound when finished

**Technical Details:**
- Uses vision model to detect obstacles, walls, edges
- Implements simple obstacle avoidance algorithm
- Maintains internal map of explored area (basic memory)

---

#### **"Find the ball"**
**Expected Outcome:**
- Activates vision object detection
- Slowly rotates 360° scanning for spherical objects
- When ball detected:
  - Plays excited beep
  - Rolls toward the ball
  - Stops 6 inches away
  - Plays victory sound
- If no ball found after 30 seconds, plays confused sound and stops

**Technical Details:**
- Vision model identifies round objects
- Prioritizes brightly colored spheres
- Distance estimation using object size in frame

---

### Interactive Commands

#### **"Come here"**
**Expected Outcome:**
- R2D2 activates vision to locate speaker
- If camera sees person:
  - Rolls toward detected person
  - Stops at 1-2 feet distance
  - Plays greeting sound
- If no person detected:
  - Spins slowly while searching
  - Plays questioning beeps
  - Times out after 15 seconds

---

#### **"Take a picture"**
**Expected Outcome:**
- R2D2 stops movement and stabilizes
- Plays camera shutter sound effect
- Captures image from front camera
- Saves to `captures/` directory with timestamp
- Plays confirmation beep
- Image filename: `r2d2_capture_YYYYMMDD_HHMMSS.jpg`

**Optional:** "Show me what you see" - displays live camera feed on connected device

---

## 👁️ Vision-Based Interaction Examples

### Object Recognition

#### **Showing R2D2 a toy or object**
**Expected Outcome:**
- Vision model identifies the object
- R2D2 announces object name with beep pattern:
  - 1 beep = recognized common object
  - 2 beeps = recognized person/face
  - 3 beeps = unknown object
- Adjusts head dome to "look" at the object
- LED color indicates confidence:
  - Green = high confidence (>80%)
  - Yellow = medium confidence (50-80%)
  - Red = low confidence (<50%)

**Example Objects:**
- Ball → single beep, tracks if moving
- Phone → single beep, neutral response
- Food item → excited beep pattern
- Another robot toy → 2 beeps, curious head tilt

---

#### **Person Detection and Tracking**
**Expected Outcome:**
- When person enters camera view:
  - Plays greeting sound
  - Dome rotates to face person
  - LEDs pulse gently
- Maintains awareness of person's position
- If person waves:
  - R2D2 waddles in response (if gesture recognition enabled)
  - Plays friendly beep

---

#### **Obstacle Avoidance**
**Expected Outcome:**
- During movement, if obstacle detected ahead:
  - Immediate stop
  - Brief pause (1 second)
  - Rotates 45° to find clear path
  - Resumes movement in new direction
- Plays cautious beep when avoiding

**Detectable Obstacles:**
- Walls and furniture
- People and pets
- Stairs and edges
- Other robots or large toys

---

### Color Recognition

#### **Holding colored object in front of R2D2**
**Expected Outcome:**
- Vision identifies dominant color
- R2D2 responds with LED matching the color:
  - Red object → red LEDs
  - Blue object → blue LEDs
  - Green object → green LEDs
  - Multi-colored → LED cycles through detected colors
- Plays melodic beep corresponding to color (different pitch per color)

**Voice Trigger:** "R2, what color is this?"

---

## 🎭 Combined Voice + Vision Examples

### **"What do you see?"**
**Voice Command + Vision Analysis**

**Expected Outcome:**
- R2D2 stops and stabilizes
- Captures current camera frame
- Vision model analyzes scene
- Responds with beep pattern indicating scene complexity:
  - Simple scene (1-2 objects): brief analytical beeps
  - Complex scene (3+ objects): longer, varied beep sequence
- LED displays:
  - Pulses during analysis
  - Final color indicates scene type:
    - Blue = indoor scene
    - Green = outdoor/nature
    - White = people present
    - Yellow = unknown/uncertain

**Console Output Example:**
```
Vision Analysis:
- Detected: person, chair, table, laptop
- Scene: indoor office environment
- Confidence: 87%
```

---

### **"Is this safe to touch?"**
**Voice Command + Object Recognition**

**Expected Outcome:**
- Analyzes object in camera view
- Classifies as safe or potentially unsafe
- Response:
  - **Safe objects** (toy, book, pillow):
    - Nods (forward-back tilt)
    - Green LED
    - Cheerful beep
  - **Unsafe objects** (sharp, hot, electrical):
    - Shakes (left-right waddle)
    - Red LED flashing
    - Warning beep pattern
    - Backs away slightly
  - **Unknown:**
    - Uncertain beep sequence
    - Yellow LED
    - No movement

---

### **"Follow the red ball"**
**Voice Trigger + Vision Tracking**

**Expected Outcome:**
- Vision filters for red spherical objects
- When detected:
  - Approaches ball slowly
  - Maintains 6-12 inch distance
  - Follows if ball moves
  - Head dome tracks ball continuously
- If ball stops:
  - R2D2 circles around it slowly
  - Plays curious beeps
- If ball disappears from view:
  - Spins 360° searching
  - Plays searching beep pattern
  - Times out after 20 seconds

---

### **"Guard this spot"**
**Voice + Vision Monitoring**

**Expected Outcome:**
- R2D2 stops at current position
- Enters sentinel mode
- Vision continuously monitors 180° forward arc
- Behavior:
  - If new object/person detected:
    - Plays alert beep sequence (loud)
    - Red LEDs flash
    - Rotates head dome to track intruder
    - Does NOT move from spot
  - If area clear:
    - Occasional soft beep (every 10 seconds)
    - Blue LED slow pulse
    - Head dome sweeps left-right periodically
- Exits on "stand down" or "stop guarding" command
- Maximum guard duration: 5 minutes (then auto-timeout)

---

### **"Play fetch"**
**Complex Interactive Mode**

**Expected Outcome:**

**Phase 1 - Ready:**
- R2D2 plays ready beep
- LED pulses green
- Vision watches for throwing motion

**Phase 2 - Object thrown:**
- Detects ball/object trajectory
- Waits for object to land
- Plays excited beep

**Phase 3 - Retrieval:**
- Rolls toward object location
- Uses vision to locate object on ground
- Approaches to within 6 inches
- Plays "found it" beep sequence

**Phase 4 - Return:**
- Spins 180° to face original position
- Rolls back to starting point
- Plays completion beeps
- Repeats from Phase 1

**Exit:** "Good boy" or "Stop playing" ends fetch mode

---

## 🔧 Diagnostic and System Commands

### **"Status report"**
**Expected Outcome:**
- R2D2 beeps battery level indicator:
  - 3 beeps = battery >66% (green LED)
  - 2 beeps = battery 33-66% (yellow LED)
  - 1 beep = battery <33% (red LED)
- Quick system check beep
- Returns to idle

**Console Output:**
```
Battery: 78%
Connection: Stable
Vision: Active
Audio: Active
Last Command: 2 seconds ago
```

---

### **"Test movement"**
**Expected Outcome:**
- Systematic movement test sequence:
  1. Roll forward 1 foot
  2. Roll backward 1 foot
  3. Strafe left
  4. Strafe right
  5. Rotate 360° clockwise
  6. Dome rotation 360°
  7. Return to start position
- Beeps at completion of each step
- Final success beep when complete
- Duration: ~25 seconds

---

### **"Sleep mode"**
**Expected Outcome:**
- R2D2 plays shutdown sound sequence
- LEDs dim to 10% brightness
- Head dome centers
- Enters low-power state
- Only responds to "wake up" command
- Minimal BLE communication

**Wake up:** "Wake up R2" restores to active mode

---

## 🎪 Advanced Scenarios

### **"Show me your tricks"**
**Automated Demo Mode**

**Expected Outcome:**
R2D2 performs a 60-second demonstration:
1. Greeting spin + happy beeps
2. Dance routine
3. Object detection demo (looks around)
4. Obstacle avoidance demo
5. Speed demo (quick acceleration)
6. Precision maneuver (figure-8 pattern)
7. Final bow (forward tilt)
8. Returns to start position

---

### **"Race mode"**
**Voice Activation**

**Expected Outcome:**
- Plays race countdown beeps: "3... 2... 1... GO!"
- Activates high-speed mode (80% max speed)
- Vision-based obstacle avoidance becomes more aggressive
- LED trails (rapid color cycling)
- Continues until "stop" or obstacle collision risk
- Speed gradually increases from 50% to 80% over 3 seconds

---

### **"Stealth mode"**
**Expected Outcome:**
- All LEDs turn off
- Movement speed reduced to 20%
- Movements become slow and deliberate
- Silent mode (beeps suppressed)
- Vision actively scans for obstacles
- Continues until "normal mode" command

---

### **"Companion mode"**
**Long-term Interactive State**

**Expected Outcome:**
- R2D2 enters persistent following behavior
- Maintains 3-5 feet distance from person
- Mimics person's movement patterns:
  - Person stops → R2D2 stops
  - Person sits → R2D2 settles (lowers stance)
  - Person walks → R2D2 follows
- Occasional autonomous behaviors:
  - Random curious beeps every 30-60 seconds
  - Head dome occasional random rotations
  - If person stationary >5 minutes, explores nearby area briefly
- Responds to all standard voice commands while in mode
- Exits on "independent mode" command

---

## 📊 Expected Behavior Reference

### Response Time Expectations
- Voice command recognition: 0.5-2 seconds
- Vision object detection: 0.2-1 second per frame
- Movement initiation: <0.3 seconds
- BLE command latency: 50-150ms

### Audio Feedback Patterns
- **Happy/Excited:** Rapid ascending beeps, high pitch
- **Sad/Confused:** Slow descending beeps, low pitch
- **Alert/Warning:** Sharp staccato beeps, alternating pitch
- **Acknowledgment:** Single mid-tone beep
- **Processing:** Soft pulsing tone
- **Error:** Three descending beeps

### LED Color Meanings
- **Blue:** Idle/listening/normal operation
- **Green:** Success/safe/go
- **Yellow:** Warning/uncertain/processing
- **Red:** Error/danger/stop
- **White:** Vision active/analyzing
- **Purple:** Special mode active
- **Cycling colors:** Entertainment/dance mode

---

## 🐛 Troubleshooting Examples

### R2D2 doesn't respond to voice commands
**Check:**
1. Microphone is enabled and permissions granted
2. Background noise level (should be <60dB)
3. Speak clearly and at moderate pace
4. Try wake word: "Hey R2" before command
5. Check console for speech recognition errors

### Vision features not working
**Check:**
1. Camera is enabled and permissions granted
2. Model files are present in `./models/` directory
3. Adequate lighting (vision works best in bright light)
4. Object is within 1-8 feet of camera
5. Check console for model loading errors

### Movement seems erratic
**Check:**
1. Battery level (low battery affects movement)
2. Clear floor space (no tangled cables or obstacles)
3. BLE connection strength
4. Calibrate by running "test movement" command

---

## 💡 Tips for Best Results

1. **Voice Commands:**
   - Speak naturally but clearly
   - Wait for acknowledgment beep before next command
   - Use wake word in noisy environments: "Hey R2, [command]"

2. **Vision Interaction:**
   - Ensure good lighting for best object recognition
   - Hold objects 2-4 feet from camera for detection
   - Allow 1-2 seconds for vision processing

3. **Movement:**
   - Clear 6-foot radius recommended for movement commands
   - Hard floors work better than carpet for rolling
   - Avoid steep inclines (>15°)

4. **Battery Management:**
   - Vision and continuous movement drain battery faster
   - Charge indicator beeps when battery drops below 20%
   - Sleep mode extends battery life between sessions

---

## 🎯 Example Session Flow

```
User: "Hey R2, wake up"
R2D2: [Startup beeps, blue LEDs activate]

User: "What do you see?"
R2D2: [Scans room, analyzes, beeps indicating detection]

User: "Follow me"
R2D2: [Acknowledges with beep, begins tracking and following]

[User walks around room]
R2D2: [Follows maintaining 3-foot distance]

User: "Stop"
R2D2: [Halts, plays acknowledgment beep]

User: "Dance R2!"
R2D2: [Performs dance routine with music and LED effects]

User: "Find the ball"
R2D2: [Rotates scanning, detects ball, rolls to it, beeps success]

User: "Good job! Sleep mode"
R2D2: [Shutdown sequence, LEDs dim, enters sleep state]
```

---

## 📝 Notes

- All timings are approximate and may vary based on system performance
- Vision accuracy depends on model quality and lighting conditions
- Battery life varies with usage intensity (typical: 45-90 minutes active use)
- Some commands may be customized or extended based on user preferences
- Command recognition may be affected by accents or speech patterns (training improves accuracy)

---

**Ready to bring R2D2 to life? Start with simple commands and build up to complex interactions!** 🚀
