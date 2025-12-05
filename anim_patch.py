import json
import os
from spherov2.commands.animatronic import Animatronic

# File to store the discovered animation ID
CONFIG_FILE = "r2_anim_config.json"

# The list of possible animation command-set IDs your R2 may require
ANIMATION_IDS = [6, 1, 0]


def _load_saved_id():
    """Load saved animation ID from JSON file."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                return data.get("anim_id")
        except:
            pass
    return None


def _save_id(anim_id):
    """Save animation ID permanently."""
    with open(CONFIG_FILE, "w") as f:
        json.dump({"anim_id": anim_id}, f)


def _try_animation(r2, anim, anim_id):
    """Attempt an animation using a specific ID."""
    try:
        pkt = Animatronic._encode(r2, anim_id, Animatronic.play_animation.__func__, anim.to_bytes(2, "big"))
        r2._execute(pkt)  # If this times out, it's the wrong ID
        return True
    except Exception as e:
        return False


def play_animation(r2, anim):
    """
    Auto-detects correct animation ID for your R2 unit.
    Saves working ID for future use.
    """

    # 1 — check if we already discovered the correct ID
    saved_id = _load_saved_id()
    if saved_id is not None:
        if _try_animation(r2, anim, saved_id):
            return True  # Works immediately

    # 2 — Try each ID until one works
    for test_id in ANIMATION_IDS:
        if _try_animation(r2, anim, test_id):
            print(f"🔥 Animation protocol matched! Using ID: {test_id}")
            _save_id(test_id)
            return True

    # 3 — No ID worked
    print("❌ ERROR: None of the animation protocols worked on your R2-D2.")
    print("This is extremely rare — please report this so we can patch more IDs.")
    return False
