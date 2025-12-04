"""
SikuliX engine wrapper (JPype). Abstrai a API Java do SikuliX para uso em Python.

Inicia JVM automaticamente (se não iniciada)

Métodos: find, click, wait, type, screenshot, read_text, exists

Usa Pattern.similar() para thresholds
Observações:

Coloque sikulixapi.jar em engine/sikulixapi.jar ou defina SIKULI_JAR_PATH ambiente.

Requer jpype1.
"""
from pathlib import Path
import jpype
import jpype.imports
from jpype.types import *
import time
from engine.config import SIKULI_JAR, SCREENSHOTS_DIR, DEFAULT_TIMEOUT

#Start JVM if needed
if not jpype.isJVMStarted():
jpype.startJVM(classpath=[str(SIKULI_JAR)])

import Sikuli classes

from org.sikuli.script import Screen, Pattern, Key # type: ignore

class SikuliEngine:
def init(self, highlight=False):
self.screen = Screen()
self.highlight = highlight

def _pattern(self, img_path, similarity=0.8):
    """Cria um Pattern com similaridade."""
    return Pattern(str(img_path)).similar(float(similarity))

def find(self, img_path, similarity=0.8, timeout=DEFAULT_TIMEOUT):
    """Retorna uma Match (obj) ou lança erro se não encontrado."""
    p = self._pattern(img_path, similarity)
    # wait retorna a match ou lança FindFailed (Java exception) -> capturamos via JPype
    try:
        m = self.screen.wait(p, float(timeout))
        return m
    except Exception as e:
        raise FileNotFoundError(f"Imagem não encontrada: {img_path} (sim={similarity}) - {e}")

def exists(self, img_path, similarity=0.8, timeout=3):
    """Retorna True/False se a imagem aparece dentro do timeout."""
    p = self._pattern(img_path, similarity)
    try:
        res = self.screen.exists(p, float(timeout))
        return bool(res)
    except Exception:
        return False

def click(self, img_path, similarity=0.8, timeout=DEFAULT_TIMEOUT):
    """Clique robusto; tenta encontrar e clicar."""
    m = self.find(img_path, similarity, timeout)
    if self.highlight:
        m.highlight(0.4)
    m.click()
    time.sleep(0.2)

def double_click(self, img_path, similarity=0.8, timeout=DEFAULT_TIMEOUT):
    m = self.find(img_path, similarity, timeout)
    if self.highlight:
        m.highlight(0.4)
    m.doubleClick()
    time.sleep(0.2)

def type(self, text):
    """Digita texto na posição atual do foco."""
    if text is None:
        return
    # convert to str for safety
    self.screen.type(str(text))
    time.sleep(0.05)

def wait(self, img_path, timeout=DEFAULT_TIMEOUT, similarity=0.8):
    return self.find(img_path, similarity, timeout)

def read_text(self, img_path, similarity=0.8, timeout=DEFAULT_TIMEOUT):
    """Localiza a imagem/região e tenta extrair texto via OCR embutido do Sikuli."""
    m = self.find(img_path, similarity, timeout)
    try:
        text = m.text()
        return str(text).strip()
    except Exception:
        return ""

def screenshot(self, name="capture"):
    """Captura screenshot e salva em reports/screenshots/<name>_<ts>.png"""
    ts = int(time.time() * 1000)
    filename = f"{name}_{ts}.png"
    out_path = SCREENSHOTS_DIR / filename
    # screen.capture() retorna ImagePath Java; usar save(dir, name) via JPype
    try:
        img = self.screen.capture()
        # algumas versões aceitam img.save(dir, name)
        img.save(str(SCREENSHOTS_DIR), filename)
    except Exception:
        # fallback: salvar via pillow (pode não estar disponível)
        try:
            img = self.screen.getScreen().capture()
            img.save(str(out_path))
        except Exception:
            # criar arquivo vazio para não quebrar fluxo
            out_path.write_bytes(b"")
    return str(out_path)