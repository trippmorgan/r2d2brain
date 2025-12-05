import asyncio
from bleak import BleakClient, BleakScanner
from .utils import build_packet

CONNECT_CHAR_UUID = "00020005-574f-4f20-5370-6865726f2121"
MAIN_CHAR_UUID = "00010002-574f-4f20-5370-6865726f2121"
HANDSHAKE_MSG = b"usetheforce...band"

def log(msg):
    """Print with immediate flush for real-time output."""
    print(msg, flush=True)

async def discover_r2d2(timeout=10.0):
    """Scan for R2D2 devices. Returns the first one found."""
    log(f"Scanning for R2-D2 (timeout: {timeout}s)...")
    devices = await BleakScanner.discover(timeout=timeout)

    for device in devices:
        name = device.name or ""
        if "D2" in name.upper() or "R2" in name.upper():
            log(f"Found R2-D2: {device.name} ({device.address})")
            return device.address

    return None

class R2D2Controller:
    def __init__(self, address=None):
        self.address = address
        self.client = None

    async def connect(self):
        # Auto-discover if no address provided
        if not self.address:
            self.address = await discover_r2d2()
            if not self.address:
                raise RuntimeError("No R2-D2 found. Make sure it's powered on and nearby.")

        log(f"Connecting to {self.address}...")
        self.client = BleakClient(self.address)
        await self.client.connect()
        await self.client.write_gatt_char(CONNECT_CHAR_UUID, HANDSHAKE_MSG)
        log("Connected!")

    async def disconnect(self):
        if self.client and self.client.is_connected:
            await self.client.disconnect()

    async def send_command(self, packet):
        await self.client.write_gatt_char(MAIN_CHAR_UUID, packet)
