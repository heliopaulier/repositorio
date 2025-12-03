import os
import random
import string
from faker import Faker

fake = Faker('pt_BR')

# ========================
# Função para gerar CPF válido
# ========================
def gerar_cpf():
    def calc_digito(digs):
        soma = sum([int(d) * w for d, w in zip(digs, range(len(digs)+1, 1, -1))])
        resto = 11 - soma % 11
        return '0' if resto > 9 else str(resto)

    cpf = [str(random.randint(0, 9)) for _ in range(9)]
    cpf.append(calc_digito(cpf))
    cpf.append(calc_digito(cpf))
    return ''.join(cpf)

# ========================
# Função para gerar dados completos
# ========================
def gerar_dados():
    return {
        "nome": fake.name(),
        "cpf": gerar_cpf(),
        "email": fake.email(),
        "telefone": fake.phone_number(),
        "endereco": fake.address().replace('\n', ', '),
        "cidade": fake.city(),
        "estado": fake.estado_sigla(),
        "cep": fake.postcode()
    }

# ========================
# Função principal para gerar arquivos TXT
# ========================
def gerar_arquivos(qtd_arquivos=5):
    base_path = os.path.dirname(os.path.abspath(__file__))
    saida_path = os.path.join(base_path, "dados_gerados")
    os.makedirs(saida_path, exist_ok=True)

    for i in range(1, qtd_arquivos + 1):
        dados = gerar_dados()
        arquivo_nome = os.path.join(saida_path, f"paciente_{i}.txt")

        with open(arquivo_nome, "w", encoding="utf-8") as f:
            for chave, valor in dados.items():
                f.write(f"{chave}: {valor}\n")

        print(f"✅ Arquivo gerado: {arquivo_nome}")

    print(f"\n✨ {qtd_arquivos} arquivos criados com sucesso na pasta 'dados_gerados'!")

# ========================
# Ponto de entrada
# ========================
if __name__ == "__main__":
    print("=== GERADOR DE DADOS DE TESTE ===")
    try:
        qtd = int(input("Quantos arquivos TXT deseja gerar? (ex: 5): "))
        gerar_arquivos(qtd)
    except ValueError:
        print("❌ Digite um número válido!")
