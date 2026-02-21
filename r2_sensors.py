#!/usr/bin/env python3
"""
R2-D2 Sensor Monitor — Real-time diagnostic display of all sensor streams.
Logs to file and prints to terminal.
"""
import sys
import time
import json
import signal
from datetime import datetime

try:
    from spherov2 import scanner
    from spherov2.sphero_edu import SpheroEduAPI, EventType
    from spherov2.toy.r2d2 import R2D2
    from spherov2.types import Color
except ImportError:
    print("❌ 'spherov2' library not installed. Run: pip install spherov2")
    sys.exit(1)

import config

running = True


def sigint_handler(sig, frame):
    global running
    running = False


def main():
    global running
    signal.signal(signal.SIGINT, sigint_handler)

    print("\n" + "=" * 40)
    print("   R2-D2 SENSOR MONITOR")
    print("=" * 40)

    print("🔍 Scanning for R2-D2...")
    toy = scanner.find_R2D2()
    if not toy:
        print("❌ R2-D2 not found.")
        return

    print(f"✅ Found: {toy.name}")

    with SpheroEduAPI(toy) as droid:
        droid.set_main_led(Color(0, 255, 0))
        print("⚡ Streaming sensors (Ctrl+C to stop)...\n")

        # Event notifications
        def on_collision(api):
            ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print(f"\n   💥 [{ts}] COLLISION!")

        def on_freefall(api):
            ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print(f"\n   🪂 [{ts}] FREEFALL!")

        def on_landing(api):
            ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print(f"\n   🛬 [{ts}] LANDING")

        droid.register_event(EventType.on_collision, on_collision)
        droid.register_event(EventType.on_freefall, on_freefall)
        droid.register_event(EventType.on_landing, on_landing)

        log_path = config.SENSOR_LOG_PATH
        count = 0
        with open(log_path, "w") as f:
            while running:
                try:
                    accel = droid.get_acceleration()
                    gyro = droid.get_gyroscope()
                    loc = droid.get_location()
                    vel = droid.get_velocity()
                    ori = droid.get_orientation()
                except Exception as e:
                    print(f"   ⚠️ Sensor read error: {e}")
                    time.sleep(config.SENSOR_POLL_RATE)
                    continue

                ts_str = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                print(
                    f"[{ts_str}] "
                    f"ACCEL x={accel.get('x',0):+.2f} y={accel.get('y',0):+.2f} z={accel.get('z',0):+.2f} | "
                    f"GYRO x={gyro.get('x',0):+.1f} y={gyro.get('y',0):+.1f} z={gyro.get('z',0):+.1f} | "
                    f"LOC x={loc.get('x',0):.0f} y={loc.get('y',0):.0f} | "
                    f"YAW={ori.get('yaw',0):.0f}"
                )

                record = {
                    "ts": time.time(),
                    "accel": accel,
                    "gyro": gyro,
                    "location": loc,
                    "velocity": vel,
                    "orientation": ori,
                    "events": [],
                }
                f.write(json.dumps(record) + "\n")
                if count % 10 == 0:
                    f.flush()
                count += 1

                time.sleep(config.SENSOR_POLL_RATE)

        print(f"\n📊 {count} readings saved to {log_path}")
        droid.set_main_led(Color(0, 0, 0))

    print("🛑 Sensor monitor stopped.")


if __name__ == "__main__":
    main()
