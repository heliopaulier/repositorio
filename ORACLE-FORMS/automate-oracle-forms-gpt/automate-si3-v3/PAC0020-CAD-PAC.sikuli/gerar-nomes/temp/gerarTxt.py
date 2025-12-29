import random

# Lê o arquivo base
with open("paciente_base.txt", "r", encoding="utf-8") as f:
    linhas = f.readlines()

# Quantos arquivos quer gerar
quantidade = int(input("Quantos arquivos deseja gerar? "))

for i in range(1, quantidade + 1):
    novo_arquivo = f"paciente_{i}.txt"
    novas_linhas = []
    for linha in linhas:
        if linha.startswith("CPF="):
            # Gera CPF aleatório válido (formato simples)
            cpf_novo = f"{random.randint(100,999)}.{random.randint(100,999)}.{random.randint(100,999)}-{random.randint(10,99)}"
            novas_linhas.append(f"CPF={cpf_novo}\n")
        else:
            novas_linhas.append(linha)
    # Salva o novo arquivo
    with open(novo_arquivo, "w", encoding="utf-8") as f_out:
        f_out.writelines(novas_linhas)
    print(f"Arquivo gerado: {novo_arquivo}")
