import cv2
import numpy as np


def match_template(screenshot, template, threshold=0.75):
    """Realiza template matching e retorna score + match."""

    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    match = max_val >= threshold

    return {
        "match": match,
        "score": float(max_val),
        "location": max_loc if match else None,
        "template_size": template_gray.shape[::-1]
    }
