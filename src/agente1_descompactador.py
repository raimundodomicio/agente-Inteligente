import os
import zipfile
import pandas as pd

class AgenteDescompactador:
    def __init__(self, caminho_zip, pasta_destino="../data"): #Função especial que inicializa o agente
        self.caminho_zip = caminho_zip
        self.pasta_destino = pasta_destino
        self.arquivo_csv = []

    def descompactar_zip(self): #Função que descompacta o arquivo ZIP e lista os arquivos CSV extraídos
        if not os.path.exists(self.pasta_destino):
            os.makedirs(self.pasta_destino)

        with zipfile.ZipFile(self.caminho_zip, 'r') as zip_temp: #Abra o arquivo ZIP em modo leitura e chama ele de zip_temp
            zip_temp.extractall(self.pasta_destino) #Extrai o arquivo zip_temp e salva em self.pasta_destino

        self.arquivo_csv = [f for f in os.listdir(self.pasta_destino) if f.endswith(".csv")] # Cria uma lista com os nomes dos arquivos .csv que estão na pasta self.pasta_destinos

        print(f"Arquivos extraídos: {self.arquivo_csv}")

    def carregar_csv(self): #Carrega os arquivos CSV em dataframes do pandas
        if not self.arquivo_csv:
            print("Nenhum arquivo CSV encontrado para carregar.")
            return {}
        dataframes = {}
        for arquivo in self.arquivo_csv:
            caminho_arquivo = os.path.join(self.pasta_destino, arquivo)
            dataframes[arquivo] = pd.read_csv(caminho_arquivo)
        
        print(f"{len(self.arquivo_csv)} arquivos CSV carregados com sucesso.")
        return dataframes

