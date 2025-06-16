import os
import pandas as pd
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Document, VectorStoreIndex
from llama_index.core import Settings

Settings.llm = None  # Desativa completamente o uso de um LLM, garantndo que toda a estrutura do agente não dependa de um LLM externo.

class AgenteIndexador:
    def __init__(self, pasta_dados="../data"): #Inicializa o agente indexador, verificando os arquivos CSV disponíveis.
        self.pasta_dados = pasta_dados
        self.index = None
        self.arquivos_csv = [f for f in os.listdir(self.pasta_dados) if f.endswith(".csv")]

    def carregar_dados(self):#Carrega os CSVs e cria um índice para buscas eficientes.
        documentos = []
        if not self.arquivos_csv:
            print("[ERRO] Nenhum arquivo CSV encontrado na pasta especificada.")
            return

        for arquivo in self.arquivos_csv:
            caminho_arquivo = os.path.join(self.pasta_dados, arquivo)
            df = pd.read_csv(caminho_arquivo)  # Carrega o CSV em um DataFrame do pandas
            print(f"Carregando dados do arquivo: {arquivo} ({len(df)} registros)")

            # Transformar cada linha em um objeto Document para busca
            for _, linha in df.iterrows():
                texto_documento = " ".join(str(valor) for valor in linha.values)  # Junta os valores em uma string
                documentos.append(Document(text=texto_documento))

        # Configurar modelo de embeddings local
        embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # Criar índice usando embeddings locais
        self.index = VectorStoreIndex.from_documents(documentos, embed_model=embed_model)
        print(f"Indexação concluída! {len(documentos)} registros foram indexados.")

    def buscar(self, consulta): #Executa busca dentro dos dados indexados.
        if not consulta:
            print("[ERRO] Consulta não pode ser vazia.")
            return
        if self.index is None:
            print("[ERRO] O índice ainda não foi criado. Execute carregar_dados() primeiro.")
            return

        motor_consulta = self.index.as_query_engine(llm=None)
        resultados = motor_consulta.query(consulta)

        
        if not resultados:
            print(f"[AVISO] Nenhum resultado encontrado para a consulta: '{consulta}'")
            return
        
        # Exibir resultados
        print(f"Resultados para '{consulta}':")
        print(f"Resultados para '{consulta}':\n")
        for node in resultados.source_nodes:
            texto_formatado = node.text.replace("\n", " ")  # Evita quebras erradas no meio das frases
            print(f"{'-'*40}\n{texto_formatado}\n{'-'*40}")

  # Lista os documentos recuperados de forma estruturada

# Teste do Agente 2
if __name__ == "__main__":
    agente = AgenteIndexador()
    agente.carregar_dados()
    agente.buscar("V CALDI PEREIRA PECAS E SERVICOS DIESEL")  # Exemplo de consulta
