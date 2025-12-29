import allure
from engine.engine import Engine

engine = Engine()


def test_cadastro_visual():
    """
    Teste inicial:
    1. Verifica campo Nome via template
    2. Verifica botão Pesquisar via template
    3. Extrai texto via OCR
    """

    with allure.step("Capturar screenshot"):
        screenshot = engine.screenshot()
        allure.attach(engine.extract_text(screenshot), "ocr_raw")

    # --- VALIDAR CAMPO NOME ---
    with allure.step("Validar presença do campo 'Nome'"):
        template = engine.load("campo_nome.png")
        result = engine.match(screenshot, template)

        allure.attach(str(result["score"]), "score_nome")
        assert result["match"], f"Campo 'Nome' não foi encontrado (score={result['score']})"

    # --- VALIDAR BOTÃO PESQUISAR ---
    with allure.step("Validar botão 'Pesquisar'"):
        template = engine.load("btn_pesquisar.png")
        result = engine.match(screenshot, template)

        allure.attach(str(result["score"]), "score_pesquisar")
        assert result["match"], f"Botão 'Pesquisar' não encontrado (score={result['score']})"

    # --- VALIDAR OCR ---
    with allure.step("Validação OCR"):
        text = engine.extract_text(screenshot)
        allure.attach(text, "ocr_output")

        assert "Pesquisa" in text or "Pesquisar" in text or "Nome" in text, \
            "Texto esperado não encontrado via OCR"
