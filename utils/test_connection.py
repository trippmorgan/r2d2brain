import asyncio
from bleak import BleakClient

# Your R2-D2 UUID
ADDRESS = "25B16450-58FD-1AC7-D75F-D9F2B6969811"

# Sphero "Anti-DOS" characteristic (Wake up)
ANTI_DOS_UUID = "00020005-574f-4f20-5370-6865726f2121"
# The magic phrase to unlock the droid
UNLOCK_CODE = b"usetheforce...band"

async def test_connect():
    print(f"Attempting to connect to {ADDRESS}...")
    
    async with BleakClient(ADDRESS) as client:
        print(f"Connected: {client.is_connected}")
        
        # 1. Send the "Unlock" phrase
        # Without this, the droid will disconnect after about 10 seconds
        print("Sending unlock code...")
        await client.write_gatt_char(ANTI_DOS_UUID, UNLOCK_CODE)
        print("Unlock code sent!")
        
        # 2. Keep alive for 5 seconds to verify it stays connected
        print("Holding connection for 5 seconds...")
        for i in range(5, 0, -1):
            print(f"{i}...")
            await asyncio.sleep(1)
            
        print("Disconnecting.")

if __name__ == "__main__":
    asyncio.run(test_connect())