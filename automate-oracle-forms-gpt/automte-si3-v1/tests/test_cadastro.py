"""
Teste avançado de cadastro de paciente:

separa passos com allure.step

captura screenshots em cada passo e anexa ao Allure

usa SikuliEngine para interação visual

usa VisionEngine para validação por template / OCR

permite trocar imagens facilmente em /images
OBS: ajuste os nomes das imagens em IMAGES map conforme seu projeto.
"""
import os
import time
import allure
from engine.config import IMAGES_DIR, SCREENSHOTS_DIR
from faker import Faker

fake = Faker()
Faker.seed(0)

mapa de imagens (nome lógico -> arquivo em images/)

IMAGES = {
"tela_inicial": IMAGES_DIR / "tela-inicial-busca-paciente.png",
"campo_pesquisa": IMAGES_DIR / "campo-pesquisa-nome.png",
"botao_pesquisar": IMAGES_DIR / "pasquisa-paciente.png",
"tela_pac_cad": IMAGES_DIR / "tela-pac-cad.png",
"botao_novo": IMAGES_DIR / "botao-novo-paciente.png",
"campo_nome": IMAGES_DIR / "area-de-texto-nome-pac.png",
"popup_nome_duplicado": IMAGES_DIR / "cadastro-de-paciente-popup-nome-diplicado2.png",
"button_popup_nao": IMAGES_DIR / "cadastro-de-paciente-popup-nome-diplicado-button-click-nao.png",
"salvar": IMAGES_DIR / "salvar-cadastro-de-paciente.png",
"popup_repetidos": IMAGES_DIR / "popup-dados-repetidos1.png",
"popup_cadastrar_novo": IMAGES_DIR / "popup-dados-repetidos-button-cadastrar-novo.png",
"indicador_sucesso": IMAGES_DIR / "indicador_cadastro_sucesso.png",
"button_sair": IMAGES_DIR / "button-sair-modulo-cadastro.png"
}

def attach_screenshot(path, name=None):
"""Anexa arquivo PNG ao Allure (se existir)."""
if path and os.path.exists(path):
with open(path, "rb") as f:
allure.attach(f.read(), name or os.path.basename(path), attachment_type=allure.attachment_type.PNG)

@allure.feature("Cadastro Paciente")
def test_cadastro_paciente_flow(sikuli, vision):
# gerar dados com Faker (evita duplicidade)
nome_paciente = (fake.first_name() + " " + fake.last_name()).upper()
nome_mae = (fake.first_name() + " " + fake.last_name()).upper()
nome_pai = (fake.first_name() + " " + fake.last_name()).upper()
cpf = fake.numerify(text="###########") # 11 digitos

# PASSO 1 - abrir tela inicial
with allure.step("Esperar tela inicial"):
    assert sikuli.exists(IMAGES["tela_inicial"], similarity=0.75, timeout=8), "Tela inicial não visível"
    p = sikuli.screenshot("01_tela_inicial")
    attach_screenshot(p, "tela_inicial")

# PASSO 2 - clicar campo pesquisa e digitar 'teste'
with allure.step("Digitar no campo de pesquisa"):
    if sikuli.exists(IMAGES["campo_pesquisa"], timeout=3):
        sikuli.click(IMAGES["campo_pesquisa"])
    else:
        # fallback: clique aproximado (ajuste se necessário)
        sikuli.click(IMAGES["tela_inicial"])
    sikuli.type("teste")
    p = sikuli.screenshot("02_apos_digitar")
    attach_screenshot(p, "apos_digitar")

# PASSO 3 - clicar pesquisar
with allure.step("Clicar pesquisar"):
    assert sikuli.exists(IMAGES["botao_pesquisar"], timeout=5), "Botao pesquisar nao encontrado"
    sikuli.click(IMAGES["botao_pesquisar"])
    p = sikuli.screenshot("03_apos_pesquisar")
    attach_screenshot(p, "apos_pesquisar")

# PASSO 4 - aguardar tela cadastro e clicar Novo
with allure.step("Aguardar tela de cadastro e clicar Novo"):
    sikuli.wait(IMAGES["tela_pac_cad"], timeout=10)
    sikuli.click(IMAGES["botao_novo"])
    time.sleep(0.5)
    p = sikuli.screenshot("04_clicou_novo")
    attach_screenshot(p, "clicou_novo")

# PASSO 5 - preencher campos principais
try:
    with allure.step("Preencher nome do paciente"):
        sikuli.double_click(IMAGES["campo_nome"])
        sikuli.type(nome_paciente)
        sikuli.type("\t")
        p = sikuli.screenshot("05_preenche_nome")
        attach_screenshot(p, "preenche_nome")

    with allure.step("Tratar popup de duplicidade (se aparecer)"):
        if sikuli.exists(IMAGES["popup_nome_duplicado"], timeout=1):
            sikuli.click(IMAGES["button_popup_nao"])
            time.sleep(0.2)

    # (demais campos: apenas exemplo — adapte sequência de tabs/inputs)
    with allure.step("Preencher nomes dos pais"):
        sikuli.type(nome_mae)
        sikuli.type("\t")
        sikuli.type(nome_pai)
        p = sikuli.screenshot("06_preenche_pais")
        attach_screenshot(p, "preenche_pais")

    with allure.step("Preencher CPF"):
        # avançar até aba documentos conforme fluxo; este é um exemplo com tabs
        sikuli.type("\t\t")  # ajustar conforme fluxo real
        sikuli.type(cpf)
        p = sikuli.screenshot("07_preenche_cpf")
        attach_screenshot(p, "preenche_cpf")

except Exception as e:
    p = sikuli.screenshot("erro_preenchimento")
    attach_screenshot(p, "erro_preenchimento")
    raise AssertionError(f"Erro no preenchimento: {e}")

# PASSO 6 - salvar e tratar popups
with allure.step("Salvar cadastro"):
    assert sikuli.exists(IMAGES["salvar"], timeout=5), "Botao salvar nao encontrado"
    sikuli.click(IMAGES["salvar"])
    time.sleep(5)
    p = sikuli.screenshot("08_apos_salvar")
    attach_screenshot(p, "apos_salvar")

    if sikuli.exists(IMAGES["popup_repetidos"], timeout=4):
        sikuli.click(IMAGES["popup_cadastrar_novo"])
        time.sleep(3)
        p2 = sikuli.screenshot("09_apos_confirmacoes")
        attach_screenshot(p2, "apos_confirmacoes")

# PASSO 7 - validação final por template (OpenCV)
with allure.step("Validacao visual por template (OpenCV)"):
    last_shot = sikuli.screenshot("10_final")
    ok, score, tl, br = vision.compare_template(last_shot, IMAGES["indicador_sucesso"], threshold=0.6)
    allure.attach(str(score), "similaridade_final")
    if not ok:
        attach_screenshot(last_shot, "final_sem_icone")
        raise AssertionError(f"Indicador de sucesso nao encontrado (score {score})")

# PASSO 8 - fechar módulo (se disponível)
with allure.step("Fechar modulo cadastro"):
    if sikuli.exists(IMAGES["button_sair"], timeout=3):
        sikuli.click(IMAGES["button_sair"])
    final = sikuli.screenshot("11_fechar")
    attach_screenshot(final, "fechar_modulo")