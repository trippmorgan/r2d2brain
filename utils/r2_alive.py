import time
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.toy.r2d2 import R2D2
from spherov2.types import Color

# ---------------------------------------------------------
# SETUP: Verified Sound Names from your log
# ---------------------------------------------------------
SOUNDS = [
    R2D2.Audio.R2_CHATTY_1,   # R2 talking
    R2D2.Audio.R2_EXCITED_3,  # R2 Excitement
    R2D2.Audio.R2_SAD_1,      # Sad sound
    R2D2.Audio.R2_SCREAM      # The famous scream
]

ANIMATIONS = [
    R2D2.Animations.EMOTE_EXCITED,
    R2D2.Animations.EMOTE_NO,
    R2D2.Animations.WWM_SCARED
]

def main():
    print("Searching for R2-D2...")
    
    # 1. Use the Generic Scanner
    toy = scanner.find_toy()
    
    if not toy:
        print("❌ R2-D2 not found. Make sure he is close and charged.")
        return

    print(f"✅ Found: {toy.name}")
    print("Connecting and Waking up...")

    # 2. Use SpheroEduAPI to handle the Wake-Up Handshake
    with SpheroEduAPI(toy) as droid:
        
        # --- LIGHTS ---
        print("💡 Testing Lights...")
        droid.set_main_led(Color(0, 0, 255)) # Blue
        time.sleep(1)
        droid.set_main_led(Color(255, 0, 0)) # Red
        time.sleep(1)

        # --- SOUNDS ---
        # 'droid.toy' gives us access to the raw R2D2 commands
        print("🔊 Testing Sounds...")
        
        for sound in SOUNDS:
            print(f"   Playing: {sound.name}")
            droid.toy.play_audio_file(sound, 1) 
            time.sleep(3) # Wait for sound to finish

        # --- ANIMATIONS ---
        print("💃 Testing Animations...")
        for anim in ANIMATIONS:
            print(f"   Acting: {anim.name}")
            droid.toy.play_animation(anim)
            time.sleep(3) # Wait for animation to finish

        # --- MOVEMENT ---
        print("🏎️  Testing Drive...")
        droid.set_main_led(Color(0, 255, 0)) # Green means Go
        
        droid.set_speed(50) # Drive Speed
        time.sleep(1)       
        
        droid.stop_roll()   # Stop
        
        # Turn head
        print("🤖 Turning Head...")
        droid.toy.turn_dome(90)
        time.sleep(1)
        droid.toy.turn_dome(-90)
        time.sleep(1)
        droid.toy.turn_dome(0)

        print("✅ Test Complete. Sleeping.")

if __name__ == "__main__":
    main()