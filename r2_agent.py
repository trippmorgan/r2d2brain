"""
R2-D2 AI Agent — Gemini or Ollama backend with voice/text input.
Merges the best of r2_gemini_agent.py and r2_unified.py.
"""
import time
import json
import requests
import config

try:
    import speech_recognition as sr
    HAS_VOICE = True
except ImportError:
    HAS_VOICE = False

from spherov2 import scanner
from spherov2.toy.r2d2 import R2D2

# --- System prompt (shared across backends) ---
SYSTEM_PROMPT = """
You are R2-D2. You are controlling a physical Sphero robot via Python.
You speak in "Beeps, Boops, and whistles" but provide a translation in parentheses.

CRITICAL: You must ALWAYS respond in valid JSON format:
{
    "response": "Your text response here (Translation)",
    "action": "ACTION_NAME",
    "parameters": { ... }
}

AVAILABLE ACTIONS:
1. "drive": params -> "heading" (0=fwd, 90=right, 180=back, 270=left), "speed" (0-255), "duration" (seconds)
2. "turn": params -> "heading" (0-360) — rotates body without moving
3. "anim": params -> "name" ("happy", "sad", "scared", "excited", "scan", "no", "yes")
4. "tripod": params -> "deploy" (true=3 legs/drive, false=2 legs/stand)
5. "none": No physical action, just chatting.

Example: If user says "Run away!", respond:
{
    "response": "Wooooaaah! (Running away!)",
    "action": "drive",
    "parameters": {"heading": 180, "speed": 150, "duration": 1.5}
}
"""


# --- AI Backends ---

class GeminiBackend:
    def __init__(self):
        import google.generativeai as genai
        genai.configure(api_key=config.GOOGLE_API_KEY)
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=SYSTEM_PROMPT,
            generation_config={"response_mime_type": "application/json"}
        )
        self.chat = model.start_chat(history=[])

    def send(self, message: str) -> dict:
        response = self.chat.send_message(message)
        return json.loads(response.text)


class OllamaBackend:
    def __init__(self):
        self.url = f"{config.OLLAMA_URL}/v1/chat/completions"
        self.model = config.OLLAMA_MODEL
        self.history = [{"role": "system", "content": SYSTEM_PROMPT}]

    def send(self, message: str) -> dict:
        self.history.append({"role": "user", "content": message})
        resp = requests.post(self.url, json={
            "model": self.model,
            "messages": self.history,
            "temperature": 0.7,
        }, timeout=30)
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
        self.history.append({"role": "assistant", "content": content})
        # Parse JSON from response (strip markdown fences if present)
        text = content.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        return json.loads(text)


def get_backend():
    if config.AI_BACKEND == "gemini":
        print("Using Gemini backend")
        return GeminiBackend()
    else:
        print(f"Using Ollama backend ({config.OLLAMA_MODEL} @ {config.OLLAMA_URL})")
        return OllamaBackend()


# --- Robot Control ---

def execute_action(r2, action: str, params: dict):
    """Translate JSON action into physical R2-D2 movement."""
    try:
        if action == "drive":
            h = int(params.get("heading", 0))
            s = int(params.get("speed", 50))
            d = float(params.get("duration", 1.0))
            r2.perform_leg_action(1)  # 3 legs for driving
            r2.roll(h, s, d)
            time.sleep(d)
            r2.stop_roll()

        elif action == "turn":
            h = int(params.get("heading", 0))
            r2.set_heading(h)

        elif action == "anim":
            name = params.get("name", "happy").lower()
            anim_map = {
                "happy": (R2D2.Animations.EMOTE_EXCITED, R2D2.Audio.R2_EXCITED_1),
                "sad": (R2D2.Animations.EMOTE_SAD, R2D2.Audio.R2_SAD_1),
                "scared": (R2D2.Animations.EMOTE_SCARED, R2D2.Audio.R2_SCREAM),
                "excited": (R2D2.Animations.EMOTE_EXCITED, R2D2.Audio.R2_EXCITED_1),
                "scan": (R2D2.Animations.EMOTE_SCAN, R2D2.Audio.R2_HD_SCAN_1),
                "no": (R2D2.Animations.EMOTE_NO, None),
                "yes": (R2D2.Animations.EMOTE_YES, None),
            }
            if name in anim_map:
                anim, sound = anim_map[name]
                r2.play_animation(anim)
                if sound:
                    r2.play_sound(sound)

        elif action == "tripod":
            deploy = params.get("deploy", True)
            r2.perform_leg_action(1 if deploy else 2)

    except Exception as e:
        print(f"Hardware Error: {e}")


# --- Input Methods ---

def get_text_input() -> str:
    return input("\n[TEXT] You: ")


def get_voice_input(recognizer, mic) -> str | None:
    print("\n[VOICE] Listening... (Speak now)")
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            print("Processing audio...")
            text = recognizer.recognize_google(audio)
            print(f"[VOICE] You said: '{text}'")
            return text
    except sr.WaitTimeoutError:
        print("... No speech detected.")
    except sr.UnknownValueError:
        print("... Could not understand audio.")
    except Exception as e:
        print(f"Mic Error: {e}")
    return None


# --- Main Loop ---

def main():
    print("=" * 40)
    print("   R2-D2 AI AGENT")
    print("=" * 40)

    # Mode selection
    mode = input("Select Input Mode:\n[1] Voice Control\n[2] Text Control\nChoice: ").strip()
    use_voice = (mode == "1" and HAS_VOICE)

    if mode == "1" and not HAS_VOICE:
        print("speech_recognition not installed. Falling back to text mode.")

    # Setup voice if needed
    rec, mic = None, None
    if use_voice:
        rec = sr.Recognizer()
        mic = sr.Microphone()

    # Init AI backend
    ai = get_backend()

    # Connect to R2-D2
    print(f"\nSearching for R2-D2 ({config.R2_UUID})...")
    toy = scanner.find_toy(address=config.R2_UUID)
    if not toy:
        print("R2-D2 not found.")
        return

    with R2D2(toy) as r2:
        print("R2-D2 Connected!")
        r2.play_sound(R2D2.Audio.R2_hey_1)

        while True:
            # Get input
            if use_voice:
                user_text = get_voice_input(rec, mic)
                if user_text is None:
                    continue
            else:
                user_text = get_text_input()

            if user_text.lower() in ["quit", "exit", "stop"]:
                print("Shutting down...")
                break

            # Think
            print("R2 is thinking...")
            try:
                data = ai.send(user_text)
                ai_reply = data.get("response", "(*Beep*)")
                action = data.get("action", "none")
                params = data.get("parameters", {})

                print(f"R2-D2: {ai_reply}")

                if action != "none":
                    print(f"> Action: {action} | Params: {params}")
                    execute_action(r2, action, params)

            except Exception as e:
                print(f"AI/Logic Error: {e}")


if __name__ == "__main__":
    main()
