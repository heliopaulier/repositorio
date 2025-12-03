# tests/conftest.py

import sys
import os
from datetime import datetime
import json
import time
import pytest
import allure
from allure_commons.types import AttachmentType
from pathlib import Path
import shutil # Adicionado para uso potencial em evidência


# =========================================================================
# 1. CORREÇÃO DE PATH E CONFIGURAÇÃO
# Garante que o Python encontre os módulos 'engine' e 'ia' (resolve ModuleNotFoundError)
# =========================================================================

# Determina o caminho para a raiz do projeto (dois níveis acima de conftest.py)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Adiciona o diretório raiz do projeto ao Python Path.
sys.path.insert(0, ROOT_DIR) 

# Diretórios
EVIDENCE_DIR = Path('sikuli/PAC020-CAD-PAC.sikuli/evidencia')
METRICS_FILE = 'reports/metrics.json'

# =========================================================================
# 2. FUNÇÃO DE REGISTRO DE MÉTRICAS
# =========================================================================

def registrar_metricas(nome_teste, duracao, status):
    """Salva métricas de tempo e status no arquivo JSON para o relatório executivo."""
    Path('reports').mkdir(exist_ok=True)
    
    if os.path.exists(METRICS_FILE):
        try:
            with open(METRICS_FILE, 'r') as f:
                metrics = json.load(f)
        except json.JSONDecodeError:
            metrics = {'test_runs': []} # Se o arquivo estiver corrompido, inicia um novo
    else:
        metrics = {'test_runs': []}
    
    metrics['test_runs'].append({
        'name': nome_teste,
        'duration': round(duracao, 2),
        'status': status,
        'timestamp': datetime.now().strftime('%Y%m%d_%H%M%S')
    })

    with open(METRICS_FILE, 'w') as f:
        json.dump(metrics, f, indent=2)


# =========================================================================
# 3. HOOK PRINCIPAL (CAPTURAR RESULTADO, TEMPO, E ANEXAR EVIDÊNCIA)
# Resolve o 'AttributeError: 'function' object has no attribute 'outcome''
# =========================================================================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Executa a chamada do teste e captura o resultado (rep)
    start_time = time.time()
    outcome = yield
    rep = outcome.get_result()
    end_time = time.time()
    
    # Processa apenas o estágio de "call" (a execução do teste em si)
    if rep.when == "call":
        status = "PASSED" if rep.passed else "FAILED"
        duration = end_time - start_time
        test_name = item.nodeid.split("::")[-1] 
        
        # 3.1. REGISTRA AS MÉTRICAS
        registrar_metricas(test_name, duration, status)

        # 3.2. ANEXA SCREENSHOT EM CASO DE FALHA (Integração Allure/Sikuli)
        if rep.failed:
            # Tenta encontrar a screenshot mais recente do Sikuli/PyAutoGUI
            try:
                # O Sikuli deve salvar o nome da falha com o timestamp
                latest_file = max(EVIDENCE_DIR.glob('*.png'), key=os.path.getmtime)
                
                # Anexa o arquivo PNG ao relatório Allure
                with open(latest_file, "rb") as f:
                    screenshot_data = f.read()

                allure.attach(
                    screenshot_data, 
                    name=f"Falha - Evidência: {latest_file.name}", 
                    attachment_type=AttachmentType.PNG
                )
            except Exception as e:
                allure.attach(f"Não foi possível anexar evidência: {e}", name="Erro de Evidência", attachment_type=AttachmentType.TEXT)