"""
Vision utilities: OpenCV template matching + pytesseract OCR helper.

compare_template: template matching (normalized)

ocr_image: pytesseract wrapper
Notas:

Requer opencv-python-headless, pytesseract e tesseract instalado no sistema.
"""
import cv2
import numpy as np
import pytesseract
from pathlib import Path

class VisionEngine:
def init(self, tesseract_cmd=None):
# se quiser apontar tesseract explicitamente, passe tesseract_cmd (ex: r"C:\Program Files\Tesseract-OCR\tesseract.exe")
if tesseract_cmd:
pytesseract.pytesseract.tesseract_cmd = str(tesseract_cmd)

def compare_template(self, screenshot_path, template_path, threshold=0.85):
    """
    Retorna (ok_bool, score_float, top_left, bottom_right)
    usa TM_CCOEFF_NORMED
    """
    scr = cv2.imread(str(screenshot_path), cv2.IMREAD_GRAYSCALE)
    tmp = cv2.imread(str(template_path), cv2.IMREAD_GRAYSCALE)
    if scr is None or tmp is None:
        return False, 0.0, None, None
    res = cv2.matchTemplate(scr, tmp, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    h, w = tmp.shape
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    return (max_val >= threshold), float(max_val), top_left, bottom_right

def ocr_image(self, image_path, lang="por"):
    """Roda pytesseract e retorna texto bruto."""
    img = cv2.imread(str(image_path))
    if img is None:
        return ""
    text = pytesseract.image_to_string(img, lang=lang)
    return text.strip()