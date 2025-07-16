import asyncio
from bleak import BleakClient
from r2d2brain.utils import build_packet

CONNECT_CHAR_UUID = "00020005-574f-4f20-5370-6865726f2121"
MAIN_CHAR_UUID = "00010002-574f-4f20-5370-6865726f2121"
HANDSHAKE_MSG = b"usetheforce...band"

class R2D2Controller:
    def __init__(self, address):
        self.address = address
        self.client = None

    async def connect(self):
        self.client = BleakClient(self.address)
        await self.client.connect()
        await self.client.write_gatt_char(CONNECT_CHAR_UUID, HANDSHAKE_MSG)

    async def send_command(self, packet):
        await self.client.write_gatt_char(MAIN_CHAR_UUID, packet)
