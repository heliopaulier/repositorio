# tests/conftest.py - pytest fixtures
import pytest, os, glob
from engine.dados_fake import gerar_paciente_dict, salvar_json
from engine.sikuli_wrapper import executar_sikuli
from engine.py_actions import screenshot

@pytest.fixture(scope='session')
def paciente():
    p = gerar_paciente_dict()
    path = 'sikuli/PAC020-CAD-PAC.sikuli/gerar-nomes/paciente_1.json'
    salvar_json(p, path)
    return p

@pytest.fixture
def attach_screenshot_on_failure(request):
    # returns a function that attaches the last evidence if test fails
    def _attach(rc, test_name='test'):
        # find latest screenshot in evidence
        evid_dir = os.path.join('sikuli','PAC020-CAD-PAC.sikuli','evidencia')
        files = sorted(glob.glob(os.path.join(evid_dir,'*.png')), key=os.path.getmtime, reverse=True)
        if files:
            latest = files[0]
            try:
                import allure
                with open(latest, 'rb') as f:
                    allure.attach(f.read(), f"evidence_{test_name}", attachment_type=allure.attachment_type.PNG)
            except Exception:
                pass
        return latest if files else None
    return _attach

@pytest.fixture
def sikuli_runner():
    def _run(script_path):
        script = os.path.abspath(script_path)
        rc, out, err = executar_sikuli(script)
        return rc, out, err
    return _run
