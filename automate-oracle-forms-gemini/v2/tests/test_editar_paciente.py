# tests/test_editar_paciente.py
import time, os, json
def test_editar_paciente(paciente, sikuli_runner, attach_screenshot_on_failure):
    start = time.time()
    rc, out, err = sikuli_runner('sikuli/PAC020-CAD-PAC.sikuli/editar_paciente.sikuli')
    duration = time.time() - start
    os.makedirs('reports', exist_ok=True)
    with open('reports/metrics.json','a') as mf:
        mf.write(json.dumps({"test":"editar","status":1 if rc==0 else 0,"duration":duration}) + "\\n")
    if rc != 0:
        attach_screenshot_on_failure(rc, 'editar')
    assert rc == 0, f"Sikuli failed: {err}"
