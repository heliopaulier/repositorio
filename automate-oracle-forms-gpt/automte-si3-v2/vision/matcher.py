import cv2
import numpy as np

def match_template(img, template):
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    _, score, _, pos = cv2.minMaxLoc(res)

    return score, pos
