
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.agente1_descompactador import AgenteDescompactador

if __name__ == "__main__":
    caminho_zip = "202401_NFs.zip"
    agente = AgenteDescompactador(caminho_zip)
    agente.descompactar_zip()
    dataframes = agente.carregar_csv()
    for nome, df in dataframes.items():
        print(f"DataFrame para {nome}:")
        print(df.head())
