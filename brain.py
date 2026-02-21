import sys
import time
import random
import threading

# --- IMPORTS ---
try:
    from spherov2 import scanner
    from spherov2.sphero_edu import SpheroEduAPI, EventType
    from spherov2.toy.r2d2 import R2D2
    from spherov2.types import Color
except ImportError:
    print("❌ Critical Error: 'spherov2' library not installed.")
    print("   Run: pip install spherov2")
    sys.exit(1)

import config

try:
    import speech_recognition as sr
    HAS_VOICE = True
except ImportError:
    print("⚠️  Warning: 'speech_recognition' not installed. Voice mode disabled.")
    HAS_VOICE = False

# --- CONFIGURATION ---
# VERIFIED MAPPINGS based on your R2-D2's internal list
ACTIONS = {
    "happy": {
        "anim": R2D2.Animations.WWM_HAPPY,    # Corrected from EMOTE_HAPPY
        "sound": R2D2.Audio.R2_EXCITED_3,
        "color": Color(255, 255, 0) # Yellow
    },
    "sad": {
        "anim": R2D2.Animations.WWM_SAD,      # Corrected from EMOTE_SAD
        "sound": R2D2.Audio.R2_SAD_1,
        "color": Color(0, 0, 255) # Blue
    },
    "scared": {
        "anim": R2D2.Animations.WWM_SCARED,
        "sound": R2D2.Audio.R2_SCREAM,
        "color": Color(255, 0, 0) # Red
    },
    "angry": {
        "anim": R2D2.Animations.WWM_ANGRY,    # Corrected from EMOTE_ANGRY
        "sound": R2D2.Audio.R2_ANNOYED,
        "color": Color(255, 0, 0)
    },
    "scan": {
        "anim": R2D2.Animations.EMOTE_SCAN,
        "sound": R2D2.Audio.R2_HEAD_SPIN,     # Corrected Sound
        "color": Color(0, 255, 0) # Green
    }
}

def main():
    print("\n" + "="*40)
    print("      R2-D2 UNIFIED BRAIN CONTROL")
    print("="*40)
    
    # 1. SETUP
    print("🔍 Scanning for R2-D2...")
    # Critical: Use find_R2D2 to get the class with audio capabilities
    toy = scanner.find_R2D2()
    
    if not toy:
        print("❌ R2-D2 not found. Check if he is charged and awake.")
        return

    print(f"✅ Found: {toy.name}")
    print("🔌 Connecting and Waking Up...")

    # Collision state
    collision_count = [0]  # mutable for closure

    def on_collision_brain(api):
        collision_count[0] += 1
        print(f"   💥 COLLISION #{collision_count[0]}!")
        try:
            api.stop_roll()
            api.set_main_led(Color(255, 0, 0))
            toy.play_audio_file(R2D2.Audio.R2_SCREAM, 0)
            time.sleep(0.5)
            # Back up
            ori = api.get_orientation()
            back = (int(ori.get("yaw", 0)) + 180) % 360
            api.roll(back, 40, 1.0)
            time.sleep(1.0)
            api.stop_roll()
            # Turn away
            new_heading = (back + random.randint(60, 120)) % 360
            api.set_heading(new_heading)
            api.set_main_led(Color(0, 0, 255))
        except Exception as e:
            print(f"   ⚠️ Collision response error: {e}")

    # 2. CONNECTION (The Hybrid Method)
    # We use SpheroEduAPI for the connection/handshake context
    with SpheroEduAPI(toy) as droid:

        # Register collision handler
        droid.register_event(EventType.on_collision, on_collision_brain)

        # --- WAKE UP ROUTINE ---
        droid.set_main_led(Color(0, 0, 255))
        # Use 'toy' for R2 specific commands
        toy.play_audio_file(R2D2.Audio.R2_HEY_1, 1)
        toy.set_head_position(0) # Center head
        print("⚡ R2-D2 is Online! (Collision detection active)")

        # 3. MODE SELECTION
        mode = ""
        while mode not in ["1", "2", "3"]:
            print("\nSelect Control Mode:")
            print("[1] Voice Control (Microphone)")
            print("[2] Text Control (Keyboard)")
            print("[3] Random/Autonomous Mode")
            mode = input("Choice: ").strip()

        if mode == "1" and HAS_VOICE:
            voice_loop(droid, toy)
        elif mode == "2":
            text_loop(droid, toy)
        elif mode == "3":
            random_loop(droid, toy)
        else:
            print("❌ Invalid choice or Voice missing. Defaulting to Text.")
            text_loop(droid, toy)

def perform_action(droid, toy, command):
    """Executes the logic for both Text and Voice modes"""
    command = command.lower()
    
    # Check our Action Dictionary
    matched = False
    for key, data in ACTIONS.items():
        if key in command:
            print(f"   🤖 Executing: {key.upper()}")
            droid.set_main_led(data["color"])
            try:
                toy.play_audio_file(data["sound"], 0) # 0 = don't wait
                toy.play_animation(data["anim"])
            except Exception as e:
                print(f"   ⚠️ Animation Error: {e}")
            matched = True
            break
    
    # Specific Movements
    if not matched:
        if "look left" in command:
            toy.set_head_position(90)
        elif "look right" in command:
            toy.set_head_position(-90)
        elif "look center" in command or "reset" in command:
            toy.set_head_position(0)
        elif "tripod" in command:
            toy.perform_leg_action(1) # 3 Legs
        elif "stand" in command:
            toy.perform_leg_action(2) # 2 Legs
        else:
            print("   ❓ R2 didn't understand.")
            toy.play_audio_file(R2D2.Audio.BB8_DONT_KNOW, 1)

def text_loop(droid, toy):
    print("\n⌨️  TEXT MODE ACTIVE")
    print("   Type 'happy', 'scan', 'look left', 'tripod', etc.")
    print("   Type 'quit' to exit.")
    
    while True:
        try:
            cmd = input("\nYou: ")
            if cmd.lower() in ["quit", "exit"]:
                break
            perform_action(droid, toy, cmd)
        except KeyboardInterrupt:
            break
    print("🛑 Disconnecting.")

def voice_loop(droid, toy):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    print("\n🎤 VOICE MODE ACTIVE")
    print("   Say 'R2 scan', 'Be happy', 'Look left'...")
    
    while True:
        try:
            with mic as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("👂 Listening...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
                
            cmd = recognizer.recognize_google(audio)
            print(f"   🗣️  You said: '{cmd}'")
            
            if "quit" in cmd.lower() or "exit" in cmd.lower():
                break
                
            perform_action(droid, toy, cmd)

        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            print("   (Silence...)")
        except KeyboardInterrupt:
            break
    print("🛑 Disconnecting.")

def random_loop(droid, toy):
    print("\n🎲 AUTONOMOUS MODE ACTIVE (Ctrl+C to stop)")
    keys = list(ACTIONS.keys())
    try:
        while True:
            action = random.choice(keys)
            print(f"   🎲 Randomly decided to: {action}")
            
            data = ACTIONS[action]
            droid.set_main_led(data["color"])
            toy.play_audio_file(data["sound"], 0)
            toy.play_animation(data["anim"])
            
            sleep_time = random.randint(5, 15)
            print(f"   Sleeping for {sleep_time}s...")
            time.sleep(sleep_time)
    except KeyboardInterrupt:
        print("🛑 Disconnecting.")

if __name__ == "__main__":
    main()