# tests/conftest.py (Adapte o código anterior para o novo caminho de evidência)

# ... (código de importação sys/os/ROOT_DIR da correção anterior) ...
# O resto do código (registrar_metricas e pytest_runtest_makereport) é o mesmo.

# ATENÇÃO: Mude a variável de diretório de evidências:
# Direciona para onde o FormsActions salva as evidências.
EVIDENCE_DIR = Path('reports/evidencia') 
METRICS_FILE = 'reports/metrics.json'

# ... (restante do código: registrar_metricas, pytest_runtest_makereport)
# tests/conftest.py

import sys
import os
from pathlib import Path  <-- ADICIONE ESTA LINHA AQUI
import json
import time
import pytest
import allure
from allure_commons.types import AttachmentType

# ... o restante do seu código (correção de ROOT_DIR, registrar_metricas, etc.)