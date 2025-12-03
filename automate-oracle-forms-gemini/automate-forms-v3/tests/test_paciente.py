# tests/test_paciente.py

import pytest
import allure
import json
from engine.sikuli_wrapper import executar_sikuli
from engine.dados_fake import gerar_paciente_dict, salvar_json
from pathlib import Path
import os
import time

# --- CONFIGURAÇÕES ---
# Note que o registro de métricas e o controle de tempo foram movidos para conftest.py
SIKULI_SCRIPT_PATH = 'sikuli/PAC020-CAD-PAC.sikuli'
SIKULI_MAIN_FILE = SIKULI_SCRIPT_PATH + '/pac020_main.py'
DADOS_PATH = Path(SIKULI_SCRIPT_PATH) / 'gerar-nomes/paciente_teste.json'


@allure.epic("Módulo de Cadastro")
@allure.feature("PAC020 - Cadastro de Paciente")
class TestCadastroPaciente:

    def setup_method(self, method):
        """
        Executado antes de cada teste.
        Responsável por gerar os dados fake e salvá-los para o Sikuli ler.
        """
        # 1. Geração de dados (Fixture ou Setup)
        self.dados_paciente = gerar_paciente_dict()
        salvar_json(self.dados_paciente, str(DADOS_PATH))
        
        with allure.step("Dados de Teste Gerados (Faker)"):
            allure.attach(
                json.dumps(self.dados_paciente, indent=2, ensure_ascii=False), 
                name="Dados Gerados", 
                attachment_type=allure.attachment_type.JSON
            )
        
        # O controle de tempo/status (start_time e self.test_name) foi movido para conftest.py


    @allure.story("CT001 - Cadastro Básico com Sucesso")
    @allure.title("Verifica o fluxo completo de inclusão de paciente")
    @allure.tag("Smoke", "Funcional")
    @pytest.mark.cadastrar
    def test_cadastro_sucesso(self):
        
        with allure.step(f"Executar Sikuli Script: {SIKULI_MAIN_FILE}"):
            # RC (Return Code) 0 = Sucesso; RC != 0 = Falha
            rc, stdout, stderr = executar_sikuli(SIKULI_MAIN_FILE) 

        # 2. Verificação do Resultado do Sikuli
        if rc != 0:
            allure.attach(f"STDOUT:\n{stdout}", name="Sikuli Log (STDOUT)", attachment_type=allure.attachment_type.TEXT)
            allure.attach(f"STDERR:\n{stderr}", name="Sikuli Log (STDERR)", attachment_type=allure.attachment_type.TEXT)
            pytest.fail(f"O script Sikuli falhou (RC: {rc}). Verifique logs e evidências anexadas.")
        
        with allure.step("Confirmação da Inclusão"):
            # O Sikuli já deve ter confirmado o sucesso internamente via OCR ou tela
            allure.attach("A automação do Sikuli confirmou a inserção do registro.", name="Status de Transação", attachment_type=allure.attachment_type.TEXT)

    # Você pode adicionar aqui o teste de edição, por exemplo:
    # @allure.story("CT002 - Edição de Telefone")
    # def test_edicao_telefone(self):
    #     # ... chama o script Sikuli para editar ...
    #     pass