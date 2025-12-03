# engine/sikuli_wrapper.py
# wrapper para executar SikuliX via subprocess

import subprocess
import os

SIKULI_JAR = r"D:\sikulix\sikulixide-2.0.5.jar" # <<<<<< AJUSTE ESTE CAMINHO

def executar_sikuli(sikuli_script_path: str, timeout: int = 600):
    sikuli_script_path = os.path.abspath(sikuli_script_path)
    cmd = ['java', '-jar', SIKULI_JAR, '-r', sikuli_script_path]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        return -1, '', 'TIMEOUT'

if __name__ == '__main__':
    # Teste de execução
    rc, out, err = executar_sikuli('sikuli/PAC020-CAD-PAC.sikuli/pac020_main.py')
    print(rc)
    print(out)
    print(err)