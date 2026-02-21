import asyncio
import sys

# Try to import the R2D2Controller from your brain.py file
try:
    from brain import R2D2Controller
except ImportError:
    print("Error: Could not import R2D2Controller from brain.py")
    print("Make sure you are in the 'r2d2brain' folder and brain.py exists.")
    sys.exit()

# Your R2-D2 UUID (verified)
ADDRESS = "25B16450-58FD-1AC7-D75F-D9F2B6969811"

async def test_movement():
    print(f"Connecting to {ADDRESS} using R2D2Controller...")
    
    # 1. Instantiate the controller
    r2 = R2D2Controller(address=ADDRESS)
    
    # 2. Connect
    await r2.connect()
    print("Connected via Controller!")

    # 3. Inspect available methods
    # This prints a list of all commands (like drive, turn_dome, etc.) available in your class
    methods = [m for m in dir(r2) if not m.startswith('__')]
    print(f"\nAvailable methods found: {methods}\n")

    # 4. Try to move the head (Dome)
    print("Attempting to move head/dome...")
    
    # We check for common method names found in R2-D2 libraries
    if "turn_dome" in methods:
        await r2.turn_dome(90)   # Turn 90 degrees
        await asyncio.sleep(1)
        await r2.turn_dome(0)    # Turn back
        print("Dome turned!")
    elif "move_head" in methods:
        await r2.move_head(90)
        await asyncio.sleep(1)
        print("Head moved!")
    elif "drive" in methods:
        print("No head command found, testing small drive wiggle...")
        # Wiggle: speed 50, heading 0, short duration
        await r2.drive(speed=50, heading=0, duration=0.5)
    else:
        print("Could not guess the movement command. Please check the 'Available methods' list above.")

    # 5. Disconnect
    print("Disconnecting...")
    await r2.disconnect()
    print("Test complete.")

if __name__ == "__main__":
    asyncio.run(test_movement())