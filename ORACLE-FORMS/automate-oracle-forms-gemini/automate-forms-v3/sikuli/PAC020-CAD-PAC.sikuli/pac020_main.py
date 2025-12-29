# pac020_main.py (Jython Sikuli Script)

# ... (Mantenha todos os Imports e Funções de Helper como estão no topo do arquivo) ...

# Constantes de Caminho (manter como estão)
# TEMPLATES = os.path.join(getBundlePath(), "templates")
# EVIDENCE = os.path.join(getBundlePath(), "evidencia")
# ...

# --- FUNÇÃO DE PESQUISA PRINCIPAL REFATORADA ---

def executar_pesquisa_paciente():
    """Função principal de automação do formulário, focada na pesquisa."""
    
    NOME_PESQUISA = "TESTE AUTOMACAO" # Valor fixo para teste de busca

    # 1. VALIDAÇÃO E PONTO DE PARTIDA (IMAGEM REFATORADA)
    log("Iniciando teste de busca...")
    try:
        # Ponto de partida refatorado para o nome da imagem fornecido
        esperar_e_clicar('tela-inicial-busca-paciente.png') 
        log("Tela 'tela-inicial-busca-paciente' encontrada e ativa.")
    except FindFailed:
        falhar_e_encerrar("Não foi possível encontrar a tela inicial de busca (tela-inicial-busca-paciente.png).")
    
    tratar_popups_comuns()

    # 2. PREENCHIMENTO DO CAMPO 'NOME'
    # O Sikuli assume que você salvou a imagem do campo 'Nome' como 'campo-nome.png'
    try:
        # Espera o campo Nome e clica para garantir o foco
        esperar_e_clicar('campo-nome.png') 
        
        # Digita o nome de teste
        type(NOME_PESQUISA)
        log(f"Digitado o nome: {NOME_PESQUISA}")
        
        # Pressionar TAB para tirar o foco (ajuste se necessário)
        type(Key.TAB) 
        
    except FindFailed:
        falhar_e_encerrar("Falha ao encontrar o campo 'Nome' para digitar.")


    # 3. CLICAR EM 'PESQUISAR'
    # O Sikuli assume que você salvou a imagem do botão 'Pesquisar' como 'botao-pesquisar.png'
    try:
        esperar_e_clicar('botao-pesquisar.png')
        log("Botão 'Pesquisar' clicado com sucesso.")
    except FindFailed:
        falhar_e_encerrar("Falha ao encontrar o botão 'Pesquisar'.")


    # 4. VERIFICAÇÃO PÓS-PESQUISA (Manter a validação de resultado)
    
    try:
        # Espera o título da tela de resultados da pesquisa
        wait('tela-resultado-pesquisa.png', 15) 
        log("Pesquisa concluída. Tela de resultados encontrada.")
    except FindFailed:
        salvar_evidencia('erro_sem_resultados')
        falhar_e_encerrar("Tela de resultados não apareceu após a pesquisa.")

    # 5. Finalização
    type(Key.ESC) # Fecha a tela de resultados/busca
    salvar_evidencia('sucesso_pesquisa_final')


# --- EXECUÇÃO DO TESTE (Manter como está) ---

if __name__ == '__main__':
    # ... (código de setup de diretórios) ...

    try:
        # Chama a função de pesquisa
        executar_pesquisa_paciente() 
        
        log("TESTE DE PESQUISA FINALIZADO COM SUCESSO (RC: 0)")
        exit(0)
    except Exception as e:
        log("Exceção geral: %s" % e)
        exit(1)