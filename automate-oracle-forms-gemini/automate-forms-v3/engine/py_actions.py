# engine/py_actions.py
# Wrappers simples sobre PyAutoGUI para ações e capturas

import pyautogui
import time
from pathlib import Path

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.25

EVIDENCE_DIR = Path('sikuli/PAC020-CAD-PAC.sikuli/evidencia')
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

def screenshot(prefix='screen'):
    ts = time.strftime('%Y%m%d_%H%M%S')
    path = str(EVIDENCE_DIR / f"{prefix}_{ts}.png")
    pyautogui.screenshot(path)
    return path

def click_xy(x, y, duration=0.2):
    pyautogui.moveTo(x, y, duration=duration)
    pyautogui.click()

def type_text(text):
    pyautogui.write(text, interval=0.03)

def press(key):
    pyautogui.press(key)