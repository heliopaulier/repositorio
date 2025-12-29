import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from engine.engine import VisionEngine
import allure


import allure
from engine.engine import VisionEngine

engine = VisionEngine()

def test_cadastro_visual():
    """
    Teste avançado que valida:
    1. Campo de nome aparece
    2. Botão SALVAR aparece
    3. OCR reconhece texto da tela
    """

    with allure.step("Capturar screenshot"):
        screenshot = engine.screenshot()

    with allure.step("Validar campo 'Nome' via template"):
        template = engine.load("campo_nome.png")
        result = engine.match(screenshot, template)

        allure.attach(str(result["score"]), "score_nome")
        assert result["match"], f"Campo NOME não encontrado — score={result['score']}"

    with allure.step("Validar botão SALVAR via template"):
        template = engine.load("btn_salvar.png")
        result = engine.match(screenshot, template)

        allure.attach(str(result["score"]), "score_salvar")
        assert result["match"], f"Botão SALVAR não encontrado — score={result['score']}"

    with allure.step("Validação OCR"):
        text = engine.extract_text(screenshot)
        allure.attach(text, "ocr_output")

        assert "Cadastro" in text, "Texto 'Cadastro' não encontrado pelo OCR"
