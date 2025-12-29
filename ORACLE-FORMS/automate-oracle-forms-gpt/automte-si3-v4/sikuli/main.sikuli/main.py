# coding: utf-8
#Nada de loop, nada de dados, nada de métricas aqui.


def safe_click(imagem):
    try:
        click(imagem)
        return True
    except FindFailed:
        capture(SCREEN)
        return False


def safe_type(texto):
    try:
        type(texto)
        return True
    except Exception:
        capture(SCREEN)
        return False


def cadastrar_paciente(nome, nome_mae, nome_pai, cpf):
    """
    Executa APENAS o cadastro do paciente.
    Não gera dados.
    Não faz loop.
    Não salva relatório.
    """

    if not safe_click("botao-novo-paciente.png"):
        return False

    safe_type(nome)
    type(Key.TAB)

    safe_type(nome_mae)
    type(Key.TAB)

    safe_type(nome_pai)
    type(Key.TAB)

    safe_type(cpf)

    return True
