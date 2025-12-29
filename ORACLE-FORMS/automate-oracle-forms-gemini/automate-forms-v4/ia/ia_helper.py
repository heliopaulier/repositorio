# ia/ia_helper.py

import sys
import cv2
import pytesseract
import numpy as np
import os
from PIL import Image

# Configurar o pytesseract (necessário se o tesseract não estiver no PATH)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def ocr_locate_by_text(path_image: str, text_to_find: str, lang: str = 'por') -> tuple:
    """
    Faz OCR na imagem e procura a bounding box do texto.
    Retorna (center_x, center_y, confidence) ou (None, None, 0)
    """
    if not os.path.exists(path_image):
        return None, None, 0

    img = cv2.imdecode(np.fromfile(path_image, dtype=np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        return None, None, 0

    # Usar output_type.DICT para obter as coordenadas de cada palavra
    data = pytesseract.image_to_data(img, lang=lang, output_type=pytesseract.Output.DICT)
    
    max_conf = 0
    
    for i in range(len(data['text'])):
        word = data['text'][i].strip()
        
        # Procura a palavra exata (case insensitive)
        if text_to_find.upper() in word.upper():
            # Obtém coordenadas
            x = data['left'][i]
            y = data['top'][i]
            w = data['width'][i]
            h = data['height'][i]
            conf = int(data['conf'][i])
            
            # Se a confiança for decente (pode ser ajustado)
            if conf > 60:
                # Calcula o centro
                center_x = x + w // 2
                center_y = y + h // 2
                
                # Retorna o primeiro match com boa confiança
                return center_x, center_y, conf
    
    return None, None, 0

if __name__ == '__main__':
    # Exemplo de teste: python ia_helper.py ocr_locate <caminho_img> <texto_busca>
    if len(sys.argv) == 4 and sys.argv[1] == 'ocr_locate':
        x, y, conf = ocr_locate_by_text(sys.argv[2], sys.argv[3])
        print(f"X:{x}, Y:{y}, Conf:{conf}")
    else:
        print("Uso: python ia_helper.py ocr_locate <caminho_img> <texto_busca>")