import time
from spherov2 import scanner
from spherov2.toy.r2d2 import R2D2
from spherov2.types import Color

print("Searching for R2-D2...")
toy = scanner.find_toy()

if not toy:
    print("❌ No R2-D2 found.")
    exit()

print("✅ Connected! Playing sounds...")

# We cast the generic 'toy' to the specific 'R2D2' class
# This gives us access to .play_audio_file()
with R2D2(toy) as droid:
    
    # 1. Light up Blue
    droid.set_main_led(Color(0, 0, 255))

    # 2. Define a list of sounds using the OFFICIAL Enums (found in step 1)
    # Note: R2-D2 often shares sound names with BB8 in the code library
    playlist = [
        R2D2.Audio.BB8_CHATTY_1,
        R2D2.Audio.BB8_HAPPY_1,
        R2D2.Audio.BB8_SCARED_1, 
        R2D2.Audio.HUM_1,
        R2D2.Audio.ION_BLAST_1
    ]

    for sound_enum in playlist:
        print(f"Playing: {sound_enum.name}")
        
        # play_audio_file(SoundID, PlayMode)
        # PlayMode 0 = Wait until done? (Depends on firmware, usually 0 or 1)
        droid.play_audio_file(sound_enum, 1) 
        
        # We sleep manually because the command might be non-blocking
        time.sleep(3)

    # Reset to Red
    droid.set_main_led(Color(255, 0, 0))
    print("Sound cycle completed.")