#Aqui você altera caminhos se mudar de PC ou diretório.

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

SIKULI_JAR = r"C:\SikuliX\sikulix.jar"
SIKULI_SCRIPT = BASE_DIR / "sikuli" / "PAC0020-CAD-PAC.sikuli"

EVIDENCE_DIR = BASE_DIR / "reports" / "evidence"
EXEC_REPORT_DIR = BASE_DIR / "reports" / "executive"

CONFIDENCE_THRESHOLD = 0.85
