                     ###PARA REALIZADO OS TESTES DEVE-SE ABRIR O MODULO E EME SEGUIDA PRESSIONAR O BOTÃO EXECUTAR###
                              ###CAMINHO: Sistema de Pacientes\Paciente\Cadastro de Pacientes (PAC0020)###

###GERA OS NOME FAKE###
# coding: utf-8
import subprocess
import time
import os

def ler_txt_com_decode(caminho):
    """
    Lê arquivo em binário e tenta decodificar em utf-8, com fallback para latin-1.
    Retorna uma lista de linhas já sem \r\n.
    Compatível com Jython (SikuliX).
    """
    with open(caminho, "rb") as f:
        conteudo_bytes = f.read()

    # remove BOM caso exista
    # em bytes o BOM UTF-8 é b'\xef\xbb\xbf'
    if conteudo_bytes.startswith(b'\xef\xbb\xbf'):
        conteudo_bytes = conteudo_bytes[len(b'\xef\xbb\xbf'):]

    # tenta decodificar para utf-8, senão latin-1
    try:
        texto = conteudo_bytes.decode('utf-8')
    except Exception:
        try:
            texto = conteudo_bytes.decode('latin-1')  # fallback comum no Windows (ANSI)
        except Exception:
            # último recurso: interpretar bytes como str direto (Python2/Jython)
            texto = str(conteudo_bytes)

    # divide em linhas de forma segura
    linhas = texto.splitlines()
    return linhas


# Exemplo de uso no seu fluxo
total_testes = 2
for i in range(total_testes):
    # Se você chama um script externo para gerar o TXT:
    subprocess.call('python "C:\\automacao\\extrair_de_excel.py" {}'.format(i), shell=True)

    caminho_arquivo = r"C:\automacao\dados_extraidos.txt"
    if not os.path.exists(caminho_arquivo):
        popup("Arquivo TXT não foi gerado para o índice {}".format(i))
        continue

    linhas = ler_txt_com_decode(caminho_arquivo)

    dados_dict = {}
    for linha in linhas:
        linha = linha.strip()
        if not linha or "=" not in linha:
            continue
        chave, valor = linha.split("=", 1)
        dados_dict[chave.strip()] = valor.strip()

    # Exemplo: pegar valores presentes no seu TXT
    nome_paciente = dados_dict.get("NomePaciente", "")
    nome_mae = dados_dict.get("NomeMae", "")
    nome_pai = dados_dict.get("NomePai", "")
    telefone = dados_dict.get("Telefone", "")
    cpf = dados_dict.get("CPF", "")

    ##popup("Rodando teste {}\nPaciente: {}\nMãe: {}\nTelefone: {}\nCPF: {}".format(
        ##i + 1, nome_paciente, nome_mae, telefone, cpf
    ##))
    time.sleep(1)


 ###CADASTRO DE PACIENTE##
#BUSCA POR NOME DO PACIENTE                            
popup("ATENCAO!!\n Para realizar este teste;  atentar-se ao pre-requiso abaixo: \n 1 - Alterar o nome do paciente \n 2 - Alterar o nome da mae \n 3 - Alterar o nome do pai \n 4 - Altetar o numero do telefone\n \nOBS: CADASTRAR NOMES SEM ACENTOS\n \n SAIR DO TESTE PRESSIONE: CTRL+ALT+C\n \nCONTUNUAR CLIQUE EM OK")
wait(3)
find("tela-inicial-busca-paciente.png")
click(Region(121,246,167,30))
type("teste")
click("pasquisa-paciente.png")
wait("tela-pac-cad.png", 10)
#CADASTRAR NOVO PACIENTE
click("botao-novo-paciente.png")
waitVanish("tela-incial-cadastro-pac.png")
doubleClick("area-de-texto-nome-pac.png")
#type(input("DIGITAR O NOME ID DO PACIENTE"))
type(nome_paciente)#ALTERAR NOME PACIENTE
type(Key.TAB)
type("NOME SOCIAL")
type(Key.TAB)
#DATA DE NASCIMENTO
type("26081978")#ALTERAR DATA DE NASCIMENTO
type(Key.TAB)
if exists("cadastro-de-paciente-popup-nome-diplicado2.png"):
    find("popup-cadastro-semelhante.png")          
    click("cadastro-de-paciente-popup-nome-diplicado-button-click-nao.png")
    wait(1)
click("tela-de-cadastro-campo-hora.png")     
type("1900")
type(Key.TAB)
type("FEMININO")
type(Key.TAB)
type("BRASILEIRA")
type(Key.TAB)
click("click-ok-nacionalidade.png")
type("SP")
type(Key.TAB)
type("SAO PAULO")
click("ok-nacionalidade-pac.png")
type(nome_mae)#ALTERAR NOME DA MAE
type(Key.TAB)
if exists("poup-cadastr-inf-nome-identico.png"):
    click("poup-cadastr-inf-nome-identico-button-nao-voltar.png")
click("campo-nome-do-pai.png")    
type(nome_pai)#ALTERAR NOME DO PAI
type(Key.TAB)
type(Key.TAB)
type(Key.TAB)
type("PARDA")
type(Key.TAB)
type("BUDISTA")
type(Key.TAB)
type("SOLTEIRO")
type(Key.TAB)
type("PROFESSOR DE MATEMATICA(ENSINO 1 GRAU)")
type(Key.TAB)
type("SEM INFORMACAO")
type(Key.TAB)
type(Key.TAB)
type("SUPERIOR COMPLETO")
type(Key.TAB)
type(Key.UP)
#CADASTRO ABA DOCUMENTOS
type(Key.TAB)
type(Key.TAB)
#click("aba-documentos-campo-conteudo.png")
#CPF
type(cpf)
type(Key.TAB)
type("SSP")
type(Key.TAB)
type("SP")
type(Key.TAB)
type("121291")
#ABA ENDERECO
click("cad-pac-aba-end.png")
click(type("aba-endereco-campo-cep.png", "05403-900"))
type(Key.TAB)
click("telacadastro-pac-aba-endereco-campo-tipo-logradouro.png")#cadastro logradouro
wait("telacadastro-pac-aba-endereco-campo-tipo-logradouro-popup-escolha.png", 5)
click(type("aba-endereco--logradouro-campo-pesquisa.png", "AVENIDA"))
click("aba-endereco--logradouro-campo-pesquisa-button-localizar.png")
click("aba-endereco--logradouro-campo-pesquisa-button-ok.png")
type(Key.TAB)
type("Dr Eneas Carvalho de Aguiar")
type(Key.TAB)
wait(6)
type("44")
wait("1728660162243.png", 12)
type(Key.TAB)
type(Key.TAB)
type(Key.TAB)
type("BRASIL")
type(Key.TAB)
type("SP")
wait(3)
click("aba-endereco-campo-lov-municipio.png")
click(type("aba-endereco-campo-lov-municipio-popup-busca.png", "SAO PAULO"))
click("aba-endereco-campo-lov-municipio-popup-busca-button-localizar.png")
click("aba-endereco-campo-lov-municipio-popup-busca-button-ok.png")
type(Key.TAB)
type(Key.TAB)
type("Cerqueira Cesar")
#ABA COMUNICACAO     
click("cad-pac-aba-comunicacao.png")
click(type("cad-pac-aba-comunicacao-campo-prioridade.png", "1"))
type(Key.TAB)
type("CELULAR")
type(Key.TAB)
type("15 98995-8564")#ALTERAR NUMERO CELULAR
type(Key.TAB)
type("CONTATO 1")
type(Key.TAB)
type(Key.TAB)
type("CADASTRO REALIZADO COM FERRAMENTA DE TESTE AUTOMATIZADO")
click("adicionar-linha-cadastro-pac-aba-cominicacao.png")
type("2")
type(Key.TAB)
type("E-MAIL")
type(Key.TAB)
type("teste@teste.com")
type(Key.TAB)
type(Key.TAB)
type(Key.TAB)
type("CADASTRO REALIZADO COM FERRAMENTA DE TESTE AUTOMATIZADO")
#SALVANDO CADASTRO
click("salvar-cadastro-de-paciente.png")  
sleep(10)
if exists("popup-dados-repetidos1.png"):
  wait("popup-informando-cadastro-parecido.png", 8)
  click("popup-dados-repetidos-button-cadastrar-novo.png")
  exists("popup-aviso-dados-duplicado.png")
  click("popup-aviso-dados-duplicado-button-sim.png")
  sleep(7)  

##GERACAO DA EVIDENCIA##
import datetime
import os
import shutil

# Caminho onde salva os prints
pasta = "d:\usuarios\helio.paulier\Meus Documentos\HELIO\ATIVIDADES\TESTES AUTOMATIZADOS_OS-387557\SIKULI\ok\ROTINAS - NOVO\ADMISSÃO-SAIDA\PAC0020-AMB.sikuli\evidencia-teste"

# Se a pasta não existir, cria
if not os.path.exists(pasta):
    os.makedirs(pasta)

# Gera o nome do arquivo com data/hora
agora = datetime.datetime.now()
nome_arquivo = "print_" + agora.strftime("%Y-%m-%d_%H-%M-%S") + ".png"

# Caminho completo do arquivo
caminho = os.path.join(pasta, nome_arquivo)

# Faz o print da tela inteira
img = capture(SCREEN)

# Move a imagem temporária para a pasta final
shutil.move(img, caminho)

print "Screenshot salvo em:", caminho


  
click("button-sair-modulo-cadastro.png")
      
      



