import os
import zipfile
import pandas as pd

class AgenteDescompactacao:
    def __init__(self, zip_path, output_folder="../data"): #Função especial que inicializa o agente
        self.zip_path = zip_path
        self.output_folder = output_folder
        self.csv_files = []

    def descompactar_zip(self): #Função que descompacta o arquivo ZIP e lista os arquivos CSV extraídos
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        with zipfile.ZipFile(self.zip_path, 'r') as zip_temp: #Abra o arquivo ZIP em modo leitura e chama ele de zip_temp
            zip_temp.extractall(self.output_folder) #Extrai o arquivo zip_temp e salva em self.output_folder

        self.csv_files = [f for f in os.listdir(self.output_folder) if f.endswith(".csv")] # Cria uma lista com os nomes dos arquivos .csv que estão na pasta self.output_folders

        print(f"Arquivos extraídos: {self.csv_files}")

    def carregar_csv(self): #Carrega os arquivos CSV em dataframes do pandas
        if not self.csv_files:
            print("Nenhum arquivo CSV encontrado para carregar.")
            return {}
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