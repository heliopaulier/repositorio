import cv2
import numpy as np
import pytesseract
import pyautogui
from pathlib import Path

class VisionEngine:
    """
    Motor de visão que encapsula:
    - Screenshot centralizado
    - Matching por template
    - OCR
    """

    def __init__(self, img_dir="images"):
        self.img_dir = Path(img_dir)

    def load(self, filename):
        """Carrega imagem interna"""
        path = self.img_dir / filename
        return cv2.imread(str(path), cv2.IMREAD_COLOR)

    def screenshot(self, region=None):
        """Tira screenshot e converte para OpenCV"""
        img = pyautogui.screenshot(region=region)
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    def match(self, screenshot, template, threshold=0.8):
        """Template Matching usando Normalized Correlation"""
        res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        return {
            "score": max_val,
            "position": max_loc,
            "match": max_val >= threshold
        }

    def extract_text(self, screenshot):
        """Extrai texto via OCR (Tesseract)"""
        gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        return pytesseract.image_to_string(gray)
