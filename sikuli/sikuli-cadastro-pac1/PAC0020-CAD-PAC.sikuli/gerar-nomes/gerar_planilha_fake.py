from faker import Faker
import unidecode
import pandas as pd
import random
import os

fake = Faker('pt_BR')

def gerar_dados(qtd=10):  # <<<<<< ALTERE A QUANTIDADE AQUI
    lista_dados = []

    for _ in range(qtd):
        nome_paciente = unidecode.unidecode(fake.name())
        nome_social = unidecode.unidecode(fake.first_name())
        data_nasc = fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%d%m%Y')
        hora_nasc = f"{random.randint(0, 23):02}{random.randint(0, 59):02}"
        sexo = random.choice(['MASCULINO', 'FEMININO'])
        nacionalidade = 'BRASILEIRA'
        nome_mae = unidecode.unidecode(fake.name_female())
        nome_pai = unidecode.unidecode(fake.name_male())
        conjuge = unidecode.unidecode(fake.name())
        responsavel = unidecode.unidecode(fake.name())
        etnia = random.choice(['BRANCA', 'PARDA', 'NEGRA', 'AMARELA', 'INDIGENA'])
        religiao = random.choice(['CATOLICO', 'EVANGELICO', 'ESPIRITA', 'BUDISTA', 'ATEU', 'OUTROS'])
        est_civil = random.choice(['SOLTEIRO', 'CASADO', 'DIVORCIADO', 'VIUVO'])
        ocupacao = unidecode.unidecode(fake.job())
        sit_familiar = random.choice(['MORA SOZINHO', 'MORA COM FAMILIA', 'MORA COM AMIGOS'])
        escolaridade = random.choice(['ENSINO FUNDAMENTAL', 'ENSINO MEDIO', 'SUPERIOR COMPLETO', 'POS-GRADUACAO'])
        rg = str(random.randint(1000000, 9999999))
        cpf = fake.cpf()
        telefone = fake.phone_number()

        dados = {
            'NomePaciente': nome_paciente,
            'NomeSocial': nome_social,
            'DataNascimento': data_nasc,
            'HoraNascimento': hora_nasc,
            'Sexo': sexo,
            'Nacionalidade': nacionalidade,
            'NomeMae': nome_mae,
            'NomePai': nome_pai,
            'Conjuge': conjuge,
            'Responsavel': responsavel,
            'Etnia': etnia,
            'Religiao': religiao,
            'EstadoCivil': est_civil,
            'Ocupacao': ocupacao,
            'SituacaoFamiliar': sit_familiar,
            'Escolaridade': escolaridade,
            'RG': rg,
            'CPF': cpf,
            'Telefone': telefone
        }

        lista_dados.append(dados)

    # Garante que a pasta exista
    os.makedirs("C:\\automacao", exist_ok=True)

    # Salva em Excel
    df = pd.DataFrame(lista_dados)
    df.to_excel("C:\\automacao\\dados_fake.xlsx", index=False)
    print(f"Planilha com {qtd} registros gerada com sucesso!")

if __name__ == "__main__":
    gerar_dados(qtd=10)  # 👈 Altere aqui se quiser mais ou menos registros
