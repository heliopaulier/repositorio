# ia/ia_visao.py
# helpers OpenCV para detecção e geração de variantes

import cv2
import numpy as np
from pathlib import Path

def template_match(screen_img, template_img, thresh=0.75):
    """Retorna bbox (x,y,w,h,conf) ou None"""
    res = cv2.matchTemplate(screen_img, template_img, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    h, w = template_img.shape[:2]
    if max_val >= thresh:
        x, y = max_loc
        return (x, y, w, h, float(max_val))
    return None

def orb_match(screen_img, template_img, min_matches=8):
    orb = cv2.ORB_create(1000)
    kp1, des1 = orb.detectAndCompute(template_img, None)
    kp2, des2 = orb.detectAndCompute(screen_img, None)
    if des1 is None or des2 is None:
        return None
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)
    if len(matches) < min_matches:
        return None
    pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1,2)
    x_min, y_min = pts.min(axis=0)
    x_max, y_max = pts.max(axis=0)
    return (int(x_min), int(y_min), int(x_max-x_min), int(y_max-y_min), len(matches))

def generate_template_variants(src_path, out_dir):
    """Gera templates variados (escala e rotação) para maior robustez do Sikuli."""
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    img = cv2.imread(str(src_path))
    if img is None:
        return 0
    h,w = img.shape[:2]
    idx = 0
    for scale in [0.95, 1.0, 1.05]:
        for angle in [-3,0,3]:
            M = cv2.getRotationMatrix2D((w/2,h/2), angle, scale)
            dst = cv2.warpAffine(img, M, (w,h))
            path = out / f"var_{idx}.png"
            cv2.imwrite(str(path), dst)
            idx += 1
    return idx