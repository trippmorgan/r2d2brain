import os
import time
import json
import google.generativeai as genai
from spherov2 import scanner
from spherov2.toy.r2d2 import R2D2

# --- CONFIGURATION ---
# PASTE YOUR API KEY HERE
GOOGLE_API_KEY = 
# YOUR SPECIFIC R2-D2 UUID
R2_UUID = "25B16450-58FD-1AC7-D75F-D9F2B6969811"

# --- GEMINI SETUP ---
genai.configure(api_key=GOOGLE_API_KEY)

# This is the "Brain" setup. We tell Gemini it is a robot controller.
sys_instruction = """
You are R2-D2. You are controlling a physical Sphero robot via Python.
You cannot speak English perfectly, you speak in "Beeps and Boops" but you can add a translation in parentheses.

CRITICAL: You must ALWAYS respond in valid JSON format with this structure:
{
    "response": "Your text response here (Beeps/Boops)",
    "action": "ACTION_NAME", 
    "parameters": { ... }
}

AVAILABLE ACTIONS:
1. "drive": params -> "heading" (0-360), "speed" (0-255), "duration" (seconds)
   - 0 is forward, 90 right, 180 back, 270 left.
2. "turn": params -> "heading" (0-360) (Just rotates the dome/body without moving)
3. "anim": params -> "name" ("happy", "sad", "scared", "excited", "scan")
4. "tripod": params -> "deploy" (true/false) (true = 3 legs/drive mode, false = 2 legs/stand)
5. "none": No physical action, just chatting.

Example: If user says "Run away!", you might output:
{
    "response": "Wooooaaah! (Running away!)",
    "action": "drive",
    "parameters": {"heading": 180, "speed": 150, "duration": 1.5}
}
"""

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash', 
    system_instruction=sys_instruction,
    generation_config={"response_mime_type": "application/json"}
)

chat = model.start_chat(history=[])

# --- ROBOT CONTROL FUNCTIONS ---
def execute_action(r2, action, params):
    if action == "drive":
        h = params.get("heading", 0)
        s = params.get("speed", 50)
        d = params.get("duration", 1.0)
        # Ensure leg is deployed for driving
        r2.perform_leg_action(1) 
        r2.roll(h, s, d)
        # roll is non-blocking usually, so we wait
        time.sleep(d) 
        r2.stop_roll()

    elif action == "turn":
        h = params.get("heading", 0)
        r2.set_heading(h) # Rotates body
        # Or rotate dome if you prefer: r2.set_head_position(angle)

    elif action == "anim":
        name = params.get("name", "happy")
        if name == "happy":
            r2.play_sound(R2D2.Audio.R2_EXCITED_1)
            r2.play_animation(R2D2.Animations.EMOTE_EXCITED)
        elif name == "sad":
            r2.play_sound(R2D2.Audio.R2_SAD_1)
            r2.play_animation(R2D2.Animations.EMOTE_SAD)
        elif name == "scared":
            r2.play_sound(R2D2.Audio.R2_SCREAM)
            r2.play_animation(R2D2.Animations.EMOTE_SCARED)
        elif name == "scan":
            r2.play_sound(R2D2.Audio.R2_HD_SCAN_1)
            r2.play_animation(R2D2.Animations.EMOTE_SCAN)

    elif action == "tripod":
        deploy = params.get("deploy", True)
        mode = 1 if deploy else 2
        r2.perform_leg_action(mode)

# --- MAIN LOOP ---
def main():
    print(f"Connecting to R2-D2 ({R2_UUID})...")
    toy = scanner.find_toy(address=R2_UUID)
    
    if not toy:
        print("R2-D2 not found.")
        return

    with R2D2(toy) as r2:
        print("\nCONNECTED! R2-D2 is online.")
        print("Type commands like 'Look around', 'Run forward', 'Do a happy dance'.")
        print("Type 'quit' to exit.")
        
        # Initial happy beep
        r2.play_sound(R2D2.Audio.R2_hey_1)

        while True:
            user_input = input("\nYou: ")
            if user_input.lower() in ["quit", "exit"]:
                break

            print("Gemini thinking...")
            
            try:
                # 1. Send to Gemini
                response = chat.send_message(user_input)
                
                # 2. Parse JSON
                # Gemini 1.5 Flash is good at JSON, but always safe to clean
                data = json.loads(response.text)
                
                ai_text = data.get("response", "...")
                action = data.get("action", "none")
                params = data.get("parameters", {})

                # 3. Print AI Response
                print(f"R2-D2: {ai_text}")
                
                # 4. Move Robot
                if action != "none":
                    print(f"DEBUG: Executing {action} with {params}")
                    execute_action(r2, action, params)
                    
            except Exception as e:
                print(f"Error processing command: {e}")

if __name__ == "__main__":
    main()