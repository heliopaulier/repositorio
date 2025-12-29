# ia/ia_visao.py

import cv2
import numpy as np
from pathlib import Path

def template_match_location(screen_path, template_path, thresh=0.8):
    """
    Encontra a localização de um template na tela usando Template Matching.
    Retorna (center_x, center_y) ou (None, None)
    """
    
    screen_img = cv2.imdecode(np.fromfile(screen_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    template_img = cv2.imdecode(np.fromfile(template_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    
    if screen_img is None or template_img is None:
        return None, None

    # Converte para tons de cinza para melhor desempenho, se não precisar de cor
    screen_gray = cv2.cvtColor(screen_img, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template_img, cv2.COLOR_BGR2GRAY)

    # Executa o Template Matching
    res = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val >= thresh:
        # Encontrado! Calcula o centro
        h, w = template_gray.shape[:2]
        top_left = max_loc
        
        center_x = top_left[0] + w // 2
        center_y = top_left[1] + h // 2
        
        return center_x, center_y
    
    return None, None