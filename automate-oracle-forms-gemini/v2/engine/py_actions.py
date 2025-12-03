# engine/py_actions.py - minimal wrapper used by pytest fixture
import pyautogui, time
from pathlib import Path
pyautogui.FAILSAFE = True; pyautogui.PAUSE = 0.25
EVIDENCE_DIR = Path('sikuli/PAC020-CAD-PAC.sikuli/evidencia'); EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
def screenshot(prefix='screen'):
    ts = time.strftime('%Y%m%d_%H%M%S')
    path = str(EVIDENCE_DIR / f"{prefix}_{ts}.png")
    pyautogui.screenshot(path)
    return path
