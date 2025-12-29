#Você executa com pytest
#O VS Code controla tudo
#Sikuli virou “plugin visual”


import time
from actions.sikuli_engine import run_sikuli
from core.metrics import Metrics

def test_pac0020():
    metrics = Metrics()

    start = time.time()
    result = run_sikuli()
    duration = time.time() - start

    metrics.add_step(
        "Cadastro de Paciente",
        "PASS" if result.returncode == 0 else "FAIL",
        duration
    )

    assert result.returncode == 0
