#✔️ Sikuli não decide nada
#✔️ Não gera relatório
#✔️ Apenas executa

import subprocess
from core.config import SIKULI_JAR, SIKULI_SCRIPT

def run_sikuli():
    """
    Executa o script Sikuli como um motor visual.
    Retorna código de execução para PyTest decidir sucesso/falha.
    """
    result = subprocess.run(
        ["java", "-jar", SIKULI_JAR, "-r", str(SIKULI_SCRIPT)],
        capture_output=True,
        text=True
    )
    return result
