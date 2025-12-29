from engine.engine import Engine
from PIL import Image, ImageDraw

engine = Engine()

def test_ocr_unitario():
    # Gera uma imagem simples com texto
    img = Image.new("RGB", (300, 100), "white")
    draw = ImageDraw.Draw(img)
    draw.text((10, 40), "Cadastro", fill="black")

    text = engine.extract_text(img)

    print("OCR Capturado:", text)

    assert "Cadastro" in text or "cadastro" in text.lower()
