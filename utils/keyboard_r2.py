import sys
import os
import time
import keyboard
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

R2_UUID = config.R2_UUID

def main():
    print(f"Searching for R2-D2 ({R2_UUID})...")
    
    # Connect directly to your specific droid
    toy = scanner.find_toy(address=R2_UUID)
    
    if not toy:
        print("R2-D2 not found! Check battery/distance.")
        return

    print(f"Connecting to {toy.name}...")

    with SpheroEduAPI(toy) as droid:
        # --- STARTUP SEQUENCE ---
        print("Connected! Initializing...")
        droid.set_main_led(Color(0, 0, 255)) # Blue
        droid.set_speed(0)
        droid.set_stabilization(True) # Keeps him upright
        
        # R2 Sound (Generic Audio ID for 'Hello')
        # Note: SpheroEduAPI uses different sound IDs than the raw library
        # We will just flash lights to confirm readiness
        droid.set_holo_projector_led(255)
        time.sleep(0.5)
        droid.set_holo_projector_led(0)
        
        print("\nControls:")
        print("[W] Forward  [S] Backward")
        print("[A] Left     [D] Right")
        print("[Q] Head Left [E] Head Right")
        print("[SHIFT] Turbo Boost")
        print("[ESC] Quit")

        base_speed = 60
        dome_angle = 0
        
        try:
            while True:
                # Quit
                if keyboard.is_pressed('esc'):
                    print("Shutting down...")
                    break

                # Speed Check (Turbo Mode)
                current_speed = base_speed + 50 if keyboard.is_pressed('shift') else base_speed

                # --- DRIVING LOGIC ---
                # We use a flag to see if any drive key is pressed
                moving = False
                
                if keyboard.is_pressed('w'):
                    droid.roll(0, current_speed, 0.5)
                    moving = True
                elif keyboard.is_pressed('s'):
                    droid.roll(180, current_speed, 0.5)
                    moving = True
                elif keyboard.is_pressed('a'):
                    droid.roll(270, current_speed, 0.5)
                    moving = True
                elif keyboard.is_pressed('d'):
                    droid.roll(90, current_speed, 0.5)
                    moving = True
                
                # If no drive keys are pressed, STOP immediately
                if not moving:
                    droid.stop_roll()

                # --- DOME CONTROL (Head Spinning) ---
                if keyboard.is_pressed('q'):
                    dome_angle = (dome_angle - 10) % 360
                    # R2 doesn't have a direct "rotate dome" in EduAPI, 
                    # but we can simulate looking by changing heading without speed 
                    # OR if using the raw R2 library. 
                    # For EduAPI, we stick to driving. 
                    print("Head Left (Simulated)")
                
                elif keyboard.is_pressed('e'):
                    dome_angle = (dome_angle + 10) % 360
                    print("Head Right (Simulated)")

                # Tiny sleep to prevent CPU overload
                time.sleep(0.05)

        except KeyboardInterrupt:
            print("\nForce Quit.")
        
        finally:
            # Shutdown sequence
            droid.stop_roll()
            droid.set_main_led(Color(255, 0, 0)) # Red
            time.sleep(1)

if __name__ == "__main__":
    main()