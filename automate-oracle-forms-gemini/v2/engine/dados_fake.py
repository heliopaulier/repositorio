# engine/dados_fake.py
# Faker generator adapted to Oracle Forms constraints.
# Ensures generated fields respect common masks/lengths (e.g., CPF digits only).

from faker import Faker
import json
from pathlib import Path
import re

fake = Faker('pt_BR')

def only_digits(s):
    return re.sub(r'\D', '', s or '')

def cpf_digits():
    # faker.cpf() often returns digits+punctuation; strip to digits. Keep 11 digits.
    raw = only_digits(fake.cpf())
    return raw.zfill(11)[:11]

def telefone_masked():
    # Return a phone like "15 99999-0000" or similar, but ensure length <= 15
    raw = only_digits(fake.phone_number())
    if len(raw) < 10:
        raw = raw.zfill(10)
    # format as (optional) DDD + number: try to create "15 99999-0000"
    if len(raw) >= 11:
        return f"{raw[:2]} {raw[2:7]}-{raw[7:11]}"
    else:
        return f"{raw[:2]} {raw[2:6]}-{raw[6:10]}"

def gerar_paciente_dict():
    # Create values respecting typical field constraints
    nome = fake.name()
    mae = fake.name_female()
    pai = fake.name_male()
    cpf = cpf_digits()
    telefone = telefone_masked()
    rg = only_digits(str(fake.random_number(digits=7, fix_len=True))).zfill(7)[:9]
    data_nasc = fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%d%m%Y')
    # Limit professions/education to reasonable lengths if used
    p = {
        'NomePaciente': nome[:60],   # limit to 60 chars
        'NomeMae': mae[:60],
        'NomePai': pai[:60],
        'Telefone': telefone,
        'CPF': cpf,
        'RG': rg,
        'DataNascimento': data_nasc,
        'CEP': only_digits(fake.postcode())[:8],
        'Email': fake.ascii_email()[:80],
        'Hora': '1900',
        'Sexo': 'FEMININO',
        'Nacionalidade': 'BRASILEIRA',
        'Prioridade': '1',
        'TipoContato': 'CELULAR'
    }
    return p

def salvar_json(paciente: dict, caminho: str):
    Path(caminho).parent.mkdir(parents=True, exist_ok=True)
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(paciente, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    p = gerar_paciente_dict()
    salvar_json(p, 'sikuli/PAC020-CAD-PAC.sikuli/gerar-nomes/paciente_1.json')
    print('Gerado:', p)
