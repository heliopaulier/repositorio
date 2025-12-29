import pytest

@pytest.fixture(scope="session", autouse=True)
def iniciar_testes():
    print("\n=== INICIANDO SUÍTE DE TESTES ===")
    yield
    print("\n=== FINALIZANDO SUÍTE DE TESTES ===")
