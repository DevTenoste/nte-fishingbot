import cv2
import numpy as np
import mss
import pyautogui
import time
import json
import os

# Disable PyAutoGUI fail-safe to prevent accidental stops, 
# but keep it if you want to stop the bot by moving mouse to corner.
pyautogui.FAILSAFE = True

class NTEFishingBot:
    def __init__(self, config_path='config.json'):
        self.config = self.load_config(config_path)
        self.sct = mss.mss()
        self.state = "IDLE"
        
        # Color ranges (HSV)
        # Note: These might need tuning based on the game's actual colors
        self.green_lower = np.array([40, 100, 100])
        self.green_upper = np.array([80, 255, 255])
        self.yellow_lower = np.array([20, 100, 100])
        self.yellow_upper = np.array([35, 255, 255])

    def load_config(self, path):
        if not os.path.exists(path):
            print(f"Error: {path} not found. Please run calibrate.py first.")
            exit(1)
        with open(path, 'r') as f:
            return json.load(f)

    def get_roi_frame(self):
        roi = self.config['bar_roi']
        monitor = {"top": int(roi['top']), "left": int(roi['left']), "width": int(roi['width']), "height": int(roi['height'])}
        img = np.array(self.sct.grab(monitor))
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    def find_horizontal_center(self, frame, lower, upper):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        moments = cv2.moments(mask)
        if moments["m00"] > 0:
            cx = int(moments["m10"] / moments["m00"])
            return cx
        return None

    def cast_line(self):
        print("Casting line...")
        pyautogui.click(self.config['button_pos']['x'], self.config['button_pos']['y'])
        time.sleep(2) # Wait for animation
        self.state = "WAITING_FOR_BITE"

    def run(self):
        print("Bot started. Press Ctrl+C to stop.")
        while True:
            if self.state == "IDLE":
                self.cast_line()

            elif self.state == "WAITING_FOR_BITE":
                # In NTE, you might need to wait for a visual cue or just wait for the bar to appear
                frame = self.get_roi_frame()
                green_center = self.find_horizontal_center(frame, self.green_lower, self.green_upper)
                if green_center is not None:
                    print("Bite detected! Starting fight...")
                    # Hook the fish
                    pyautogui.click(self.config['button_pos']['x'], self.config['button_pos']['y'])
                    self.state = "FIGHTING"
                time.sleep(0.1)

            elif self.state == "FIGHTING":
                frame = self.get_roi_frame()
                green_center = self.find_horizontal_center(frame, self.green_lower, self.green_upper)
                yellow_center = self.find_horizontal_center(frame, self.yellow_lower, self.yellow_upper)

                if green_center is None:
                    # Bar disappeared, fight ended
                    print("Fight ended.")
                    self.state = "IDLE"
                    pyautogui.keyUp('a')
                    pyautogui.keyUp('d')
                    time.sleep(3) # Wait for catch animation
                    continue

                if yellow_center is not None:
                    diff = yellow_center - green_center
                    threshold = 10 # Pixels

                    if diff > threshold:
                        pyautogui.keyDown('a')
                        pyautogui.keyUp('d')
                    elif diff < -threshold:
                        pyautogui.keyDown('d')
                        pyautogui.keyUp('a')
                    else:
                        pyautogui.keyUp('a')
                        pyautogui.keyUp('d')
                
                time.sleep(0.01) # High frequency for fight

if __name__ == "__main__":
    bot = NTEFishingBot()
    try:
        bot.run()
    except KeyboardInterrupt:
        print("\nStopping bot...")
        pyautogui.keyUp('a')
        pyautogui.keyUp('d')
