# ia/ia_helper.py
# CLI helper for OCR and lightweight popup detection.
# Called from Sikuli (Jython) via subprocess because Jython can't use native OpenCV/Tesseract.
import sys
import cv2
import pytesseract
import numpy as np

# If tesseract binary is not in PATH, set the path here, e.g.:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def ocr_image(path_image: str, lang: str = 'por') -> str:
    # Read image robustly even with unicode path
    img = cv2.imdecode(np.fromfile(path_image, dtype=np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        return ''
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    config = '--psm 6'
    text = pytesseract.image_to_string(th, lang=lang, config=config)
    return text.strip()

def detect_popup_by_ratio(path_image: str) -> str:
    img = cv2.imdecode(np.fromfile(path_image, dtype=np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        return 'NORMAL'
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    white = cv2.countNonZero(th)
    total = h * w
    ratio = white / float(total)
    if ratio > 0.35:
        return 'POSSIVEL_POPUP'
    return 'NORMAL'

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('ERR'); sys.exit(1)
    cmd = sys.argv[1]; img = sys.argv[2]
    if cmd == 'ocr':
        print(ocr_image(img))
    elif cmd == 'popup':
        print(detect_popup_by_ratio(img))
    else:
        print('UNKNOWN')
