import os
import pandas as pd
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Document, VectorStoreIndex
from llama_index.core import Settings

# Desativa uso de LLM remoto
Settings.llm = None

class AgenteIndexador:
    def __init__(self, pasta_dados="../data"):
        self.pasta_dados = pasta_dados
        self.index = None
        self.dados_estruturados = pd.DataFrame()
        self.arquivos_csv = [
            f for f in os.listdir(self.pasta_dados) if f.endswith(".csv")
        ]

    def carregar_dados(self): #Carrega arquivos CSV e constrói o índice vetorial
        documentos = []
        frames = []

        if not self.arquivos_csv:
            print("[ERRO] Nenhum arquivo CSV encontrado na pasta especificada.")
            return

        for arquivo in self.arquivos_csv:
            caminho_arquivo = os.path.join(self.pasta_dados, arquivo)
            df = pd.read_csv(caminho_arquivo)
            print(f"Carregando dados do arquivo: {arquivo} ({len(df)} registros)")

            # Armazena dados estruturados (para busca por nota fiscal)
            frames.append(df)

            # Cria documentos para indexação semântica
            for _, linha in df.iterrows():
                texto = " ".join(str(valor) for valor in linha.values)
                documentos.append(Document(text=texto))

        # Une todos os dados estruturados em um único DataFrame
        self.dados_estruturados = pd.concat(frames, ignore_index=True)

        # Cria índice vetorial para buscas abertas
        embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.index = VectorStoreIndex.from_documents(documentos, embed_model=embed_model)
        print(f"Indexação concluída! {len(documentos)} registros foram indexados.")

    def buscar_por_numero_nf(self, numero_nf): #Busca estruturada por nota fiscal
        if self.dados_estruturados.empty:
            print("[ERRO] Dados ainda não foram carregados.")
            return []

        # Converte para string e procura ocorrência parcial em qualquer coluna
        filtrado = self.dados_estruturados[
            self.dados_estruturados.apply(
                lambda row: str(numero_nf) in row.astype(str).to_list(), axis=1
            )
        ]

        return filtrado.to_dict(orient="records")

    def buscar_semantico(self, consulta): #Busca por similaridade semântica
        if not consulta:
            print("[ERRO] Consulta não pode ser vazia.")
            return []
        if self.index is None:
            print("[ERRO] O índice ainda não foi criado. Execute carregar_dados() primeiro.")
            return []

        motor = self.index.as_query_engine(llm=None)
        resultados = motor.query(consulta)

        if not resultados:
            print(f"[AVISO] Nenhum resultado encontrado para: '{consulta}'")
            return []

        # Extrai textos dos nós encontrados
        documentos = [node.text.replace("\n", " ") for node in resultados.source_nodes]
        return documentos


# Teste isolado do Agente 2
if __name__ == "__main__":
    agente = AgenteIndexador()
    agente.carregar_dados()

    print("\nConsulta estruturada por número da NF:")
    notas = agente.buscar_por_numero_nf("5183")
    for nota in notas:
        print(f"- {nota}")

    print("\nConsulta semântica (livre):")
    textos = agente.buscar_semantico("comprador de peças diesel")
    for t in textos:
        print(f"\n{t}\n{'-'*40}")
