import asyncio
import cv2
from r2d2brain.ble_controller import R2D2Controller
from r2d2brain.voice import recognizer, mic
from r2d2brain.vision import load_model

async def main():
    load_model()
    r2d2 = R2D2Controller(address="XX:XX:XX:XX:XX:XX")
    await r2d2.connect()
    print("Connected to R2D2")

    while True:
        with mic as source:
            audio = recognizer.listen(source, timeout=1, phrase_time_limit=3)
            try:
                text = recognizer.recognize_google(audio)
                print("Heard:", text)
            except Exception as e:
                print("Recognition error:", e)
        await asyncio.sleep(0.1)
