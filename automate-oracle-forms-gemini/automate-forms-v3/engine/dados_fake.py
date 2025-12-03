# engine/dados_fake.py
# Faker para geração de dados de paciente

from faker import Faker
import json
from pathlib import Path

fake = Faker('pt_BR')

def gerar_paciente_dict():
    """Gera um dicionário com campos usados pelo formulário, com limites de caracteres."""
    p = {
        'NomePaciente': fake.name()[:30], # Limite 30
        'NomeMae': fake.name_female()[:30], # Limite 30
        'NomePai': fake.name_male()[:30], # Limite 30
        'Telefone': fake.phone_number()[:15].replace('(', '').replace(')', '').replace('-', '').replace(' ', ''),
        'CPF': fake.cpf(),
        'RG': str(fake.random_number(digits=7, fix_len=True)),
        'DataNascimento': fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%d%m%Y'),
        'CEP': fake.postcode().replace('-', ''), # Remove hífen
        'Email': fake.ascii_email()[:50], # Limite 50
        'Hora': '1900',
        'Sexo': 'FEMININO',
        'Nacionalidade': 'BRASILEIRA'
    }
    return p

def salvar_json(paciente: dict, caminho: str):
    Path(caminho).parent.mkdir(parents=True, exist_ok=True)
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(paciente, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    # Gera um arquivo JSON para o Sikuli usar no teste
    p = gerar_paciente_dict()
    salvar_json(p, 'sikuli/PAC020-CAD-PAC.sikuli/gerar-nomes/paciente_1.json')
    print('Gerado:', p)