import pyautogui
import time
import json
import os

def calibrate():
    print("=== NTE Fishing Bot Calibration ===")
    print("Instructions:")
    print("1. Open Neverness to Everness and start a fishing session.")
    print("2. Hover your mouse over the TOP-LEFT corner of the fishing bar UI.")
    print("3. Wait 5 seconds...")
    time.sleep(5)
    top_left = pyautogui.position()
    print(f"Captured Top-Left: {top_left}")

    print("\n4. Hover your mouse over the BOTTOM-RIGHT corner of the fishing bar UI.")
    print("5. Wait 5 seconds...")
    time.sleep(5)
    bottom_right = pyautogui.position()
    print(f"Captured Bottom-Right: {bottom_right}")

    print("\n6. Hover your mouse over the 'CAST/HOOK' button.")
    print("7. Wait 5 seconds...")
    time.sleep(5)
    button_pos = pyautogui.position()
    print(f"Captured Button Position: {button_pos}")

    config = {
        "bar_roi": {
            "top": top_left.y,
            "left": top_left.x,
            "width": bottom_right.x - top_left.x,
            "height": bottom_right.y - top_left.y
        },
        "button_pos": {
            "x": button_pos.x,
            "y": button_pos.y
        }
    }

    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)
    
    print("\nCalibration saved to config.json!")
    print(json.dumps(config, indent=4))

if __name__ == "__main__":
    try:
        calibrate()
    except KeyboardInterrupt:
        print("\nCalibration cancelled.")
