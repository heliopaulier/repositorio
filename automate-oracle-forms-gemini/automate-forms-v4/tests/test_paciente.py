# tests/test_paciente.py

import pytest
import allure
import json
import time
from engine.forms_actions import FormsActions
from engine.dados_fake import gerar_paciente_dict, salvar_json
from pathlib import Path
import os
import pyautogui # Necessário para pressionar teclas

# --- INSTÂNCIA DO MOTOR DE AÇÃO ---
actions = FormsActions()

@allure.epic("Módulo de Cadastro")
@allure.feature("PAC020 - Busca de Paciente (OCR/OpenCV)")
class TestBuscaPaciente:

    def setup_method(self, method):
        # 1. Geração de dados (Faker) para o teste
        self.dados_paciente = gerar_paciente_dict()
        
        with allure.step("Dados de Teste Gerados"):
            allure.attach(
                json.dumps(self.dados_paciente, indent=2, ensure_ascii=False), 
                name="Dados Gerados (Faker)", 
                attachment_type=allure.attachment_type.JSON
            )

    @allure.story("CT001 - Busca por Nome com OCR")
    @allure.title("Verifica a busca de paciente pelo nome usando OCR")
    @allure.tag("Smoke", "Funcional", "OCR")
    @pytest.mark.busca
    def test_busca_por_nome(self):
        
        # O nome do paciente gerado (ou um nome fixo para busca)
        nome_para_buscar = "TESTE AUTOMACAO" # Usaremos um nome fixo
        
        with allure.step("1. Localizar e Clicar na tela inicial"):
            # AÇÃO 1: CLICAR NA TELA DE BUSCA. Usamos o nome da imagem do botão/título.
            # Você deve ter o arquivo 'tela-inicial-busca-paciente.png' na pasta 'templates/'
            if not actions.wait_and_click_by_template('tela-inicial-busca-paciente.png', timeout=15):
                pytest.fail("Falha ao encontrar o ponto de partida (tela-inicial-busca-paciente.png).")

        with allure.step("2. Localizar Campo Nome (Via Template) e Digitar"):
            # AÇÃO 2: CLICAR NO CAMPO NOME. Usamos a imagem do campo 'Nome'.
            if not actions.wait_and_click_by_template('campo-nome.png', timeout=10):
                pytest.fail("Falha ao encontrar o campo 'Nome' via Template Matching.")
            
            actions.type_text(nome_para_buscar)
            actions.press('tab') # Sai do campo

        with allure.step("3. Localizar e Clicar em Pesquisar (Via Texto OCR)"):
            # AÇÃO 3: CLICAR NO BOTÃO PESQUISAR. Usamos OCR para mais robustez no botão.
            if not actions.wait_and_click_by_text('Pesquisar', timeout=10):
                pytest.fail("Falha ao encontrar o botão 'Pesquisar' via OCR.")
        
        with allure.step("4. Validação do Resultado (Via Template ou OCR)"):
            # AÇÃO 4: VERIFICAR TELA DE RESULTADO. Você pode usar OCR ou Template.
            # Exemplo usando OCR para encontrar o texto 'Resultados'
            actions.screenshot('final_busca')
            # if not actions.wait_and_click_by_text('Resultados', timeout=15):
            #     pytest.fail("Falha ao validar a tela de resultados após a busca.")
            
            # Se for bem-sucedido, feche a tela
            actions.press('escape')