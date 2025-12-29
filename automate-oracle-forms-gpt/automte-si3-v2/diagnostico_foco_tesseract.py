import os
import pytesseract
from PIL import Image, ImageDraw

print("===== DIAGNÓSTICO TESSERACT =====")

# Caminhos
print("\nTesseract CMD:", pytesseract.pytesseract.tesseract_cmd)
print("TESSDATA_PREFIX:", os.environ.get("TESSDATA_PREFIX"))

# Verifica idioma POR
tessdata = os.environ.get("TESSDATA_PREFIX", "")
por_path = os.path.join(tessdata, "por.traineddata")

print("\nArquivo por.traineddata existe?")
print("OK" if os.path.exists(por_path) else "NÃO ENCONTRADO ❌")

# Cria uma imagem de teste
img = Image.new("RGB", (300, 100), "white")
draw = ImageDraw.Draw(img)
draw.text((10, 40), "Teste OCR Português", fill="black")

# Testa OCR
print("\nRodando OCR...")
try:
    txt = pytesseract.image_to_string(img, lang="por")
    print("OCR Resultado:", txt.strip())
except Exception as e:
    print("❌ OCR FALHOU:", e)

print("\n===== FIM DO DIAGNÓSTICO =====")
