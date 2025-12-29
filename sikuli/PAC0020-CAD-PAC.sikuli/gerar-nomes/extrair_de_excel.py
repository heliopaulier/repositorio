import pandas as pd
import sys
import os

def salvar_dados_paciente(index=0):
    df = pd.read_excel("C:\\automacao\\dados_fake.xlsx")

    if index >= len(df):
        print("Índice fora do limite.")
        return

    paciente = df.iloc[index]
    
    with open("C:\\automacao\\dados_extraidos.txt", "w", encoding="utf-8") as f:
        f.write("NomePaciente={}\n".format(paciente['NomePaciente']))
        f.write("NomeMae={}\n".format(paciente['NomeMae']))
        f.write("NomePai={}\n".format(paciente['NomePai']))
        f.write("Telefone={}\n".format(paciente['Telefone']))
        f.write("CPF={}\n".format(paciente['CPF']))
        f.write("RG={}\n".format(paciente['RG']))
        
    print("Paciente {} salvo com sucesso.".format(index + 1))

if __name__ == "__main__":
    index = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    salvar_dados_paciente(index)
