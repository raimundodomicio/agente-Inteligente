import os
import zipfile
import pandas as pd

class AgenteDescompactacao:
    def __init__(self, zip_path, output_folder="../data"):
        self.zip_path = zip_path
        self.output_folder = output_folder
        self.csv_files = []

    def descompactar_zip(self):
        """Descompacta o arquivo ZIP e lista os arquivos CSV extraídos."""
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.output_folder)

        # Lista os arquivos CSV extraídos
        self.csv_files = [f for f in os.listdir(self.output_folder) if f.endswith(".csv")]

        print(f"Arquivos extraídos: {self.csv_files}")

    def carregar_csv(self):
        """Carrega os arquivos CSV em dataframes do pandas."""
        dataframes = {}
        for file in self.csv_files:
            file_path = os.path.join(self.output_folder, file)
            dataframes[file] = pd.read_csv(file_path)
        
        print(f"{len(self.csv_files)} arquivos CSV carregados com sucesso.")
        return dataframes

# Exemplo de uso
if __name__ == "__main__":
    zip_path = "../202401_NFs.zip"  # Caminho do ZIP no diretório raiz
    agente = AgenteDescompactacao(zip_path)
    agente.descompactar_zip()
    dataframes = agente.carregar_csv()