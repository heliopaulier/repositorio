from core.runner import executar_cadastro

def test_cadastro_paciente_basico():
    resultado = executar_cadastro("PACIENTE TESTE")

    assert resultado["ok"] is True
    assert resultado["paciente"] == "PACIENTE TESTE"
