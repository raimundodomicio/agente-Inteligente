from src.agente_descompactacao import AgenteDescompactacao
from src.agente_indexador import AgenteIndexador
from src.agente_interpretador import AgenteInterpretador

class AgenteExecutor:
    def __init__(self):
        """Inicializa os agentes"""
        self.descompactador = AgenteDescompactacao(caminho_zip="202401_NFs.zip", pasta_destino="../data")
        self.indexador = AgenteIndexador()
        self.interpretador = AgenteInterpretador()

    def executar_pipeline(self, pergunta):
        """Processa a pergunta do usuário e busca dados"""
        consulta = self.interpretador.interpretar_pergunta(pergunta)
        
        if consulta:
            print(f"Buscando '{consulta['campo']}' na nota fiscal {consulta['filtro']}...")
            resultados = self.indexador.buscar(consulta['filtro'])  # Executa consulta no Agente 2
            
            return resultados
        else:
            return "⚠ Pergunta não compreendida."

# Teste do Executor
if __name__ == "__main__":
    executor = AgenteExecutor()
    pergunta_teste = "Quais os itens vendidos na nota fiscal 3482?"
    resposta = executor.executar_pipeline(pergunta_teste)
    print(f"🛠 Resultado Final:\n{resposta}")
