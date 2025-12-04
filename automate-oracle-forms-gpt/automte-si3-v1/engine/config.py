from pathlib import Path
import os

#Configurações centrais do projeto
ROOT = Path(file).parent.parent.resolve()
IMAGES_DIR = ROOT / "images"
REPORTS_DIR = ROOT / "reports"
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"
SIKULI_JAR = Path(os.environ.get("SIKULI_JAR_PATH", Path(file).parent / "sikulixapi.jar")).resolve()

#empo padrão de espera (segundos)
DEFAULT_TIMEOUT = 10

#Garantir diretórios
CREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
