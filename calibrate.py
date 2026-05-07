import pyautogui
import json
import os
import time
import keyboard # New dependency for global hotkeys

# To handle High DPI screens on Windows
try:
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

def get_point(prompt):
    print(f"\n[?] {prompt}")
    print("    --> Placez votre souris et appuyez sur [F8] dans le jeu...")
    
    # Global wait for F8 key
    keyboard.wait('f8')
    
    pos = pyautogui.position()
    print(f"    [OK] Capturé : {pos.x}, {pos.y}")
    
    # Small delay to avoid double triggers
    time.sleep(0.5)
    return pos

def calibrate():
    print("=== NTE Fishing Bot Calibration (Mode F8) ===")
    print("Instructions : Gardez le jeu ouvert. Pas besoin de changer de fenêtre !")
    print("Utilisez la touche [F8] pour valider chaque position.\n")
    
    top_left = get_point("Etape 1: Coin HAUT-GAUCHE de la zone de la barre de pêche")
    bottom_right = get_point("Etape 2: Coin BAS-DROIT de la zone de la barre de pêche")
    button_pos = get_point("Etape 3: Position du bouton LANCER/FERRER")

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

    # Validation simple
    if config['bar_roi']['width'] <= 0 or config['bar_roi']['height'] <= 0:
        print("\n[!] ERREUR : La zone sélectionnée est invalide. Recommencez.")
        return

    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)
    
    print("\n[SUCCESS] Configuration enregistrée dans config.json !")
    print(json.dumps(config, indent=4))
    print("\nVous pouvez maintenant fermer cette fenêtre et lancer le bot.")

if __name__ == "__main__":
    try:
        calibrate()
    except KeyboardInterrupt:
        print("\nAnnulé.")
