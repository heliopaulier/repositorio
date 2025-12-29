"""
Fixtures globais e ajuste PYTHONPATH para evitar ModuleNotFoundError.
Adiciona a raiz do projeto ao sys.path quando os testes rodarem a partir de tests/.
"""
import sys
import os
from pathlib import Path
import pytest

ROOT = Path(file).parent.parent.resolve()
if str(ROOT) not in sys.path:
sys.path.insert(0, str(ROOT))

from engine.sikuli_engine import SikuliEngine
from engine.vision_engine import VisionEngine

@pytest.fixture(scope="session")
def sikuli():
"""Instancia o motor Sikuli (um por sessão)."""
engine = SikuliEngine(highlight=False)
yield engine
# opcional: cleanup se necessário
try:
import jpype
if jpype.isJVMStarted():
jpype.shutdownJVM()
except Exception:
pass

@pytest.fixture(scope="session")
def vision():
"""Instancia VisionEngine (OpenCV + Tesseract)."""
# Se precisar passar caminho do tesseract: VisionEngine(tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe")
return VisionEngine()
