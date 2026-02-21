#!/usr/bin/env python3
"""
R2-D2 Autonomous Explorer — Roams, detects collisions, logs all sensor data,
and generates a summary report.
"""
import sys
import time
import json
import math
import random
import signal
import threading
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

# ── Colours ──────────────────────────────────────────────────────────────────
GREEN = Color(0, 255, 0)
RED = Color(255, 0, 0)
YELLOW = Color(255, 255, 0)
BLUE = Color(0, 0, 255)
OFF = Color(0, 0, 0)


class Explorer:
    """Manages autonomous exploration with full sensor logging."""

    def __init__(self):
        self.running = False
        self.sensor_thread = None
        self.start_time = 0.0
        self.positions = []          # (x, y) trail
        self.collisions = []         # list of dicts
        self.freefalls = []
        self.events_queue = []       # pending events for next sensor tick
        self.collision_count = 0
        self.freefall_count = 0
        self.max_accel = 0.0
        self.max_accel_time = 0.0
        self.max_gyro = 0.0
        self.max_gyro_time = 0.0
        self.max_speed = 0.0
        self.total_distance = 0.0
        self.last_loc = None
        self.lock = threading.Lock()

    # ── Event handlers ───────────────────────────────────────────────────
    def on_collision(self, api):
        ts = time.time()
        try:
            loc = api.get_location()
            vel = api.get_velocity()
            ori = api.get_orientation()
        except Exception:
            loc = {"x": 0, "y": 0}
            vel = {"x": 0, "y": 0}
            ori = {"yaw": 0}
        speed = math.hypot(vel.get("x", 0), vel.get("y", 0))
        entry = {
            "ts": ts,
            "location": loc,
            "heading": ori.get("yaw", 0),
            "speed": speed,
        }
        with self.lock:
            self.collisions.append(entry)
            self.collision_count += 1
            self.events_queue.append({"type": "collision", **entry})
        print(f"   💥 COLLISION at ({loc['x']:.0f}, {loc['y']:.0f})")

    def on_freefall(self, api):
        ts = time.time()
        with self.lock:
            self.freefall_count += 1
            self.freefalls.append({"ts": ts})
            self.events_queue.append({"type": "freefall", "ts": ts})
        print("   🪂 FREEFALL detected!")

    def on_landing(self, api):
        with self.lock:
            self.events_queue.append({"type": "landing", "ts": time.time()})
        print("   🛬 LANDING detected")

    def on_gyro_max(self, api):
        with self.lock:
            self.events_queue.append({"type": "gyro_max", "ts": time.time()})
        print("   🌀 EXTREME ROTATION")

    # ── Sensor streaming thread ──────────────────────────────────────────
    def sensor_loop(self, droid):
        with open(config.SENSOR_LOG_PATH, "w") as f:
            while self.running:
                try:
                    accel = droid.get_acceleration()
                    gyro = droid.get_gyroscope()
                    location = droid.get_location()
                    velocity = droid.get_velocity()
                    orientation = droid.get_orientation()
                except Exception:
                    time.sleep(config.SENSOR_POLL_RATE)
                    continue

                ts = time.time()

                # Track stats
                accel_mag = math.sqrt(
                    accel.get("x", 0) ** 2 +
                    accel.get("y", 0) ** 2 +
                    accel.get("z", 0) ** 2
                )
                gyro_mag = math.sqrt(
                    gyro.get("x", 0) ** 2 +
                    gyro.get("y", 0) ** 2 +
                    gyro.get("z", 0) ** 2
                )
                speed = math.hypot(velocity.get("x", 0), velocity.get("y", 0))

                with self.lock:
                    if accel_mag > self.max_accel:
                        self.max_accel = accel_mag
                        self.max_accel_time = ts
                    if gyro_mag > self.max_gyro:
                        self.max_gyro = gyro_mag
                        self.max_gyro_time = ts
                    if speed > self.max_speed:
                        self.max_speed = speed

                    # Distance tracking
                    cur = (location.get("x", 0), location.get("y", 0))
                    if self.last_loc is not None:
                        dx = cur[0] - self.last_loc[0]
                        dy = cur[1] - self.last_loc[1]
                        self.total_distance += math.hypot(dx, dy)
                    self.last_loc = cur
                    self.positions.append(cur)

                    # Grab queued events
                    events = list(self.events_queue)
                    self.events_queue.clear()

                record = {
                    "ts": ts,
                    "accel": accel,
                    "gyro": gyro,
                    "location": location,
                    "velocity": velocity,
                    "orientation": orientation,
                    "events": events,
                }
                f.write(json.dumps(record) + "\n")
                f.flush()

                time.sleep(config.SENSOR_POLL_RATE)

    # ── Exploration algorithm ────────────────────────────────────────────
    def explore(self, droid, toy):
        self.running = True
        self.start_time = time.time()

        # Register events
        droid.register_event(EventType.on_collision, self.on_collision)
        droid.register_event(EventType.on_freefall, self.on_freefall)
        droid.register_event(EventType.on_landing, self.on_landing)
        droid.register_event(EventType.on_gyro_max, self.on_gyro_max)

        # Start sensor thread
        self.sensor_thread = threading.Thread(
            target=self.sensor_loop, args=(droid,), daemon=True
        )
        self.sensor_thread.start()

        # Deploy tripod for driving
        print("   🦿 Deploying tripod legs...")
        try:
            toy.perform_leg_action(1)
        except Exception:
            pass
        time.sleep(1)

        droid.set_main_led(GREEN)
        print("   🟢 Exploring! Press Ctrl+C to stop.\n")

        deadline = self.start_time + config.EXPLORATION_DURATION
        heading = 0

        try:
            while self.running and time.time() < deadline:
                # Roll forward
                speed = random.randint(
                    max(30, config.EXPLORATION_SPEED - 15),
                    min(80, config.EXPLORATION_SPEED + 15),
                )
                duration = random.uniform(1.5, 3.0)
                droid.set_main_led(GREEN)
                droid.roll(heading, speed, duration)
                time.sleep(duration)
                droid.stop_roll()

                # Check for recent collision — if so, react
                recent_collision = False
                with self.lock:
                    if self.collisions and (time.time() - self.collisions[-1]["ts"]) < 2.0:
                        recent_collision = True

                if recent_collision:
                    droid.set_main_led(RED)
                    try:
                        toy.play_audio_file(R2D2.Audio.R2_SCREAM, 0)
                    except Exception:
                        pass
                    # Back up
                    back_heading = (heading + 180) % 360
                    droid.roll(back_heading, 40, 1.0)
                    time.sleep(1.0)
                    droid.stop_roll()
                    # Turn away
                    heading = (heading + random.randint(90, 270)) % 360
                    droid.set_heading(heading)
                    time.sleep(0.5)
                    droid.set_main_led(GREEN)
                else:
                    # Random new heading
                    heading = random.randint(0, 360)
                    droid.set_heading(heading)
                    time.sleep(0.3)

                # Log position
                try:
                    loc = droid.get_location()
                    print(
                        f"   📍 ({loc.get('x', 0):.0f}, {loc.get('y', 0):.0f}) "
                        f"hdg={heading}° spd={speed}"
                    )
                except Exception:
                    pass

        except KeyboardInterrupt:
            pass

        self.running = False
        droid.stop_roll()
        droid.set_main_led(BLUE)
        try:
            toy.play_audio_file(R2D2.Audio.R2_SAD_1, 1)
        except Exception:
            pass

        if self.sensor_thread:
            self.sensor_thread.join(timeout=2)

        self.generate_report()

    # ── Report generation ────────────────────────────────────────────────
    def generate_report(self):
        duration = time.time() - self.start_time
        with self.lock:
            positions = list(self.positions)
            collisions = list(self.collisions)
            collision_count = self.collision_count
            freefall_count = self.freefall_count
            max_speed = self.max_speed
            max_accel = self.max_accel
            max_accel_time = self.max_accel_time
            max_gyro = self.max_gyro
            max_gyro_time = self.max_gyro_time
            total_distance = self.total_distance

        # Bounding box
        if positions:
            xs = [p[0] for p in positions]
            ys = [p[1] for p in positions]
            bbox = (max(xs) - min(xs)) * (max(ys) - min(ys))
            bbox_str = f"{max(xs)-min(xs):.0f} x {max(ys)-min(ys):.0f} = {bbox:.0f} sq units"
        else:
            bbox_str = "N/A"

        # Collision table
        coll_rows = ""
        for c in collisions:
            t = datetime.fromtimestamp(c["ts"]).strftime("%H:%M:%S")
            loc = c.get("location", {})
            coll_rows += (
                f"| {t} | ({loc.get('x', 0):.0f}, {loc.get('y', 0):.0f}) "
                f"| {c.get('heading', 0):.0f}° | {c.get('speed', 0):.1f} |\n"
            )

        # Position trail (sample if too many)
        trail = positions[::max(1, len(positions) // 50)] if positions else []
        trail_str = "\n".join(f"- ({p[0]:.0f}, {p[1]:.0f})" for p in trail)

        report = f"""# R2-D2 Exploration Report

## Summary
- **Duration:** {duration:.1f}s
- **Distance traveled:** {total_distance:.1f} units
- **Collisions:** {collision_count}
- **Freefalls:** {freefall_count}
- **Max speed:** {max_speed:.1f}
- **Area covered:** {bbox_str}
- **Sensor readings logged:** {len(positions)}

## Collision Log
| Time | Location (x,y) | Heading | Speed |
|------|----------------|---------|-------|
{coll_rows if coll_rows else "| — | — | — | — |"}

## Sensor Highlights
- **Max acceleration:** {max_accel:.2f} g's at {datetime.fromtimestamp(max_accel_time).strftime('%H:%M:%S') if max_accel_time else 'N/A'}
- **Max rotation:** {max_gyro:.1f} deg/s at {datetime.fromtimestamp(max_gyro_time).strftime('%H:%M:%S') if max_gyro_time else 'N/A'}

## Position Trail
{trail_str if trail_str else "No positions recorded."}
"""
        with open(config.REPORT_PATH, "w") as f:
            f.write(report)
        print(f"\n📊 Report saved to {config.REPORT_PATH}")
        print(f"📈 Sensor log at {config.SENSOR_LOG_PATH}")


def main():
    print("\n" + "=" * 40)
    print("   R2-D2 AUTONOMOUS EXPLORER")
    print("=" * 40)
    print(f"   Duration: {config.EXPLORATION_DURATION}s")
    print(f"   Speed: {config.EXPLORATION_SPEED}")
    print(f"   Sensor rate: {config.SENSOR_POLL_RATE}s\n")

    print("🔍 Scanning for R2-D2...")
    toy = scanner.find_R2D2()
    if not toy:
        print("❌ R2-D2 not found.")
        return

    print(f"✅ Found: {toy.name}")
    print("🔌 Connecting...")

    explorer = Explorer()

    # Allow Ctrl+C to stop gracefully
    def sigint_handler(sig, frame):
        explorer.running = False
    signal.signal(signal.SIGINT, sigint_handler)

    with SpheroEduAPI(toy) as droid:
        droid.set_main_led(BLUE)
        try:
            toy.play_audio_file(R2D2.Audio.R2_HEY_1, 1)
        except Exception:
            pass
        print("⚡ R2-D2 Online!\n")
        explorer.explore(droid, toy)

    print("🛑 Explorer shut down.")


if __name__ == "__main__":
    main()
