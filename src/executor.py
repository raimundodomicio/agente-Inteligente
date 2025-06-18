# src/agente_executor.py

from src.agente_descompactador import AgenteDescompactador
from src.agente_indexador import AgenteIndexador
from src.agente_interpretador import AgenteInterpretador
from langchain.schema import Document

class AgenteExecutor:
    def __init__(self): #Inicializa os agentes.
        caminho_zip = "202401_NFs.zip"  # Caminho do ZIP no diretório raiz
        self.descompactador = AgenteDescompactador(caminho_zip)
        self.indexador = AgenteIndexador()
        self.interpretador = AgenteInterpretador()

    def executar_pipeline(self, pergunta):#Processa a pergunta do usuário e busca dados com resposta natural.
        consulta = self.interpretador.interpretar_pergunta(pergunta)

        if consulta:
            print(f"Buscando '{consulta['campo']}' na nota fiscal {consulta['filtro']}...")

            # Indexador retorna documentos formatados
            self.indexador.carregar_dados()
            documentos = self.indexador.buscar(consulta['filtro'])

            # Gera resposta usando LangChain com o modelo do interpretador
            resposta = self.interpretador.chain.run(
                input_documents=documentos,
                question=pergunta
            )

            return resposta
        else:
            return "Pergunta não compreendida."

# Teste do AgenteExecutor
if __name__ == "__main__":
    executor = AgenteExecutor()
    perguntas = [
        "Qual o valor total da nota fiscal 369180?",
        "Quais os itens vendidos na nota fiscal 17055?",
        "Quem foi o comprador na NF 5183?"
    ]

    for pergunta in perguntas:
        resposta = executor.executar_pipeline(pergunta)
        print(f"Resposta Gerada:{resposta}\n")
