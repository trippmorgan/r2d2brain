#!/usr/bin/env python3
"""Entry point for the R2-D2 Brain project."""

def main():
    print("\n" + "=" * 40)
    print("      R2-D2 BRAIN — MAIN MENU")
    print("=" * 40)
    print("[1] AI Agent (Voice/Text + Sensors)")
    print("[2] Explorer (Autonomous Roaming)")
    print("[3] Sensor Monitor (Diagnostics)")
    print("[4] Brain (Manual Control)")
    print()

    choice = input("Choice: ").strip()

    if choice == "1":
        from r2_agent import main as agent_main
        agent_main()
    elif choice == "2":
        from r2_explorer import main as explorer_main
        explorer_main()
    elif choice == "3":
        from r2_sensors import main as sensor_main
        sensor_main()
    elif choice == "4":
        from brain import main as brain_main
        brain_main()
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
