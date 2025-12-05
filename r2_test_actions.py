
import asyncio
import sys

# Try to import the R2D2Controller from your brain.py file
try:
    from brain import R2D2Controller
except ImportError:
    print("Error: Could not import R2D2Controller from brain.py")
    sys.exit()

# Your R2-D2 UUID
ADDRESS = "25B16450-58FD-1AC7-D75F-D9F2B6969811"

async def test_functionality():
    print(f"Connecting to {ADDRESS}...")
    
    r2 = R2D2Controller(address=ADDRESS)
    await r2.connect()
    print("Connected!")

    # 1. Print all available commands
    # This helps us see what your specific library can do
    methods = [m for m in dir(r2) if not m.startswith('__')]
    print(f"\nAvailable Commands: {methods}\n")

    # 2. Try to turn on LIGHTS
    print("Attempting to turn on lights...")
    if "set_main_led" in methods:
        # Try standard Sphero format (r, g, b)
        try:
            await r2.set_main_led(0, 0, 255) # Blue
            print("Command sent: set_main_led (Blue)")
        except:
            # Try passing a Color object if the library requires it
            from spherov2.types import Color
            await r2.set_main_led(Color(0, 0, 255))
            print("Command sent: set_main_led (Color Object)")
    elif "set_color" in methods:
        await r2.set_color(0, 0, 255)
        print("Command sent: set_color")
    else:
        print("Could not find a light command in the list above.")

    # 3. Try to move HEAD (Dome)
    print("Attempting to move head...")
    if "turn_dome" in methods:
        await r2.turn_dome(90)
        await asyncio.sleep(1)
        await r2.turn_dome(0)
        print("Dome moved!")
    elif "move_head" in methods:
        await r2.move_head(90)
        print("Head moved!")
    else:
        print("Could not find a head movement command.")

    # 4. Play a Sound (if available)
    if "play_sound" in methods:
        print("Attempting to play sound...")
        # ID 3 is typically a happy beep
        await r2.play_sound(3) 

    # Keep alive for 3 seconds to observe
    await asyncio.sleep(3)
    
    print("Disconnecting...")
    await r2.disconnect()
    print("Test complete.")

if __name__ == "__main__":
    asyncio.run(test_functionality())