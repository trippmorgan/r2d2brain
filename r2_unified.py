import os
import time
import json
import asyncio
import threading
import google.generativeai as genai
import speech_recognition as sr
from spherov2 import scanner
from spherov2.toy.r2d2 import R2D2

# --- CONFIGURATION ---
GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY_HERE"  # <--- PASTE KEY
R2_UUID = "25B16450-58FD-1AC7-D75F-D9F2B6969811"

# --- GEMINI AI SETUP ---
genai.configure(api_key=GOOGLE_API_KEY)

# We tell Gemini how to behave and force JSON output for control
SYS_INSTRUCTION = """
You are R2-D2. You are controlling a physical Sphero robot.
You speak in "Beeps, Boops, and whistles" but provide a translation in parentheses.

CRITICAL: You must ALWAYS respond in valid JSON format:
{
    "response": "Your text response here (Translation)",
    "action": "ACTION_NAME", 
    "parameters": { ... }
}

ACTIONS:
1. "drive": params -> "heading" (0=fwd, 180=back), "speed" (0-255), "duration" (sec)
2. "anim": params -> "name" ("happy", "sad", "scared", "excited", "scan", "no", "yes")
3. "turn": params -> "heading" (0-360)
4. "none": No movement, just chatting.
"""

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash', 
    system_instruction=SYS_INSTRUCTION,
    generation_config={"response_mime_type": "application/json"}
)

chat_session = model.start_chat(history=[])

# --- ROBOT BODY (The Hardware Layer) ---
def execute_robot_action(r2, action, params):
    """Translates JSON instructions into physical movement"""
    try:
        if action == "drive":
            h = int(params.get("heading", 0))
            s = int(params.get("speed", 50))
            d = float(params.get("duration", 1.0))
            r2.perform_leg_action(1) # Ensure 3 legs for driving
            r2.roll(h, s, d)
            # We assume non-blocking roll; sleep manualy to let it complete
            time.sleep(d) 
            r2.stop_roll()

        elif action == "anim":
            name = params.get("name", "happy").lower()
            if name == "happy":
                r2.play_animation(R2D2.Animations.EMOTE_HAPPY)
                r2.play_sound(R2D2.Audio.R2_EXCITED_1)
            elif name == "sad":
                r2.play_animation(R2D2.Animations.EMOTE_SAD)
                r2.play_sound(R2D2.Audio.R2_SAD_1)
            elif name == "scared":
                r2.play_animation(R2D2.Animations.EMOTE_SCARED)
                r2.play_sound(R2D2.Audio.R2_SCREAM)
            elif name == "scan":
                r2.play_animation(R2D2.Animations.EMOTE_SCAN)
            elif name == "no":
                r2.play_animation(R2D2.Animations.EMOTE_NO)
            elif name == "yes":
                r2.play_animation(R2D2.Animations.EMOTE_YES)

        elif action == "turn":
            h = int(params.get("heading", 0))
            r2.drive_with_heading(0, h, 0) # Rotate in place

    except Exception as e:
        print(f"Hardware Error: {e}")

# --- INPUT LAYER (The Ears/Keyboard) ---
def get_text_input():
    return input("\n[TEXT] You: ")

def get_voice_input(recognizer, mic):
    print("\n[VOICE] Listening... (Speak now)")
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            # Timeout = wait 5s for sound. phrase_time_limit = max 5s of speaking
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            print("Processing audio...")
            text = recognizer.recognize_google(audio)
            print(f"[VOICE] You said: '{text}'")
            return text
    except sr.WaitTimeoutError:
        print("... No speech detected.")
        return None
    except sr.UnknownValueError:
        print("... Could not understand audio.")
        return None
    except Exception as e:
        print(f"Mic Error: {e}")
        return None

# --- MAIN BRAIN LOOP ---
def main():
    print("--- R2-D2 UNIFIED BRAIN ---")
    
    # 1. Mode Selection
    mode = input("Select Input Mode:\n[1] Voice Control (Kids Mode)\n[2] Text Control (Dev Mode)\nChoice: ")
    use_voice = (mode == "1")

    # 2. Setup Audio if needed
    rec = None
    mic = None
    if use_voice:
        rec = sr.Recognizer()
        mic = sr.Microphone()

    # 3. Connect to Robot
    print(f"\nSearching for Droid ({R2_UUID})...")
    toy = scanner.find_toy(address=R2_UUID)
    if not toy:
        print("R2-D2 not found.")
        return

    with R2D2(toy) as r2:
        print("R2-D2 Connected!")
        r2.play_sound(R2D2.Audio.R2_hey_1) # Greeting sound

        while True:
            # A. Get Input
            user_text = ""
            if use_voice:
                user_text = get_voice_input(rec, mic)
                if user_text is None:
                    continue # Loop back and listen again
            else:
                user_text = get_text_input()
            
            if user_text.lower() in ["quit", "exit", "stop"]:
                print("Shutting down...")
                break

            # B. Think (Gemini)
            print("R2 is thinking...")
            try:
                response = chat_session.send_message(user_text)
                data = json.loads(response.text)
                
                ai_reply = data.get("response", "(*Beep*)")
                action = data.get("action", "none")
                params = data.get("parameters", {})

                # C. Respond (Print + Robot Action)
                print(f"R2-D2: {ai_reply}")
                
                if action != "none":
                    print(f"> Action: {action} | Params: {params}")
                    execute_robot_action(r2, action, params)
                
            except Exception as e:
                print(f"AI/Logic Error: {e}")

if __name__ == "__main__":
    main()