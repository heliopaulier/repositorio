# gerarTxt.py
# coding: utf-8
import random
import os

# Caminho da pasta onde os arquivos serão salvos
base_path = os.path.dirname(__file__)
saida_path = os.path.join(base_path, "dados_gerados")

# Cria a pasta se não existir
if not os.path.exists(saida_path):
    os.makedirs(saida_path)

# Função para gerar um CPF válido
def gerar_cpf():
    numeros = [random.randint(0, 9) for _ in range(9)]
    for _ in range(2):
        soma = sum([(len(numeros)+1-i) * n for i, n in enumerate(numeros)])
        resto = soma % 11
        numeros.append(0 if resto < 2 else 11 - resto)
    return "{}{}{}.{}{}{}.{}{}{}-{}{}".format(*numeros)

# Listas básicas
nomes = ["Ana", "Maria", "João", "Carlos", "Fernanda", "Lucas", "Juliana", "Ricardo", "Patrícia", "Gabriel"]
sobrenomes = ["Silva", "Souza", "Pereira", "Almeida", "Ferreira", "Costa", "Oliveira", "Moura", "Montenegro", "Cavalcante"]

# Função para gerar um paciente
def gerar_paciente():
    nome = f"{random.choice(['Dr.', 'Dra.', ''])} {random.choice(nomes)} {random.choice(sobrenomes)}"
    mae = f"{random.choice(nomes)} {random.choice(sobrenomes)}"
    pai = f"{random.choice(nomes)} {random.choice(sobrenomes)}"
    telefone = f"{random.randint(11, 99)} {random.randint(1000,9999)}-{random.randint(1000,9999)}"
    cpf = gerar_cpf()
    rg = random.randint(1000000, 9999999)
    return {
        "NomePaciente": nome.strip(),
        "NomeMae": mae,
        "NomePai": pai,
        "Telefone": telefone,
        "CPF": cpf,
        "RG": rg
    }

# Pergunta quantos arquivos deseja gerar
qtd = int(input("Quantos arquivos TXT deseja gerar? "))

for i in range(1, qtd + 1):
    paciente = gerar_paciente()
    nome_arquivo = os.path.join(saida_path, f"paciente_{i}.txt")
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(f"NomePaciente={paciente['NomePaciente']}\n")
        f.write(f"NomeMae={paciente['NomeMae']}\n")
        f.write(f"NomePai={paciente['NomePai']}\n")
        f.write(f"Telefone={paciente['Telefone']}\n")
        f.write(f"CPF={paciente['CPF']}\n")
        f.write(f"RG={paciente['RG']}\n")
    print(f"Arquivo gerado: {nome_arquivo}")

print(f"\n✅ {qtd} arquivos TXT criados com sucesso na pasta: {saida_path}")
4