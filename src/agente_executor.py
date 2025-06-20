from src.agente1_descompactador import AgenteDescompactador
from src.agente2_indexador import AgenteIndexador
from src.agente3_interpretador import AgenteInterpretador

class AgenteExecutor: #Inicializa os agentes
    def __init__(self):
        self.descompactador = AgenteDescompactador(caminho_zip="202401_NFs.zip", pasta_destino="../data")
        self.indexador = AgenteIndexador()
        self.interpretador = AgenteInterpretador()

    def executar_pipeline(self, pergunta):  # Processa a pergunta do usuário e busca dados
        consulta = self.interpretador.interpretar_pergunta(pergunta)
    
        if consulta:
            print(f"Buscando '{consulta['campo']}' na nota fiscal {consulta['filtro']}...")

            self.indexador.carregar_dados()  # Garante que os dados estejam prontos antes da busca
            resultados = self.indexador.buscar(consulta['filtro'])  # Executa consulta no Agente 2

            if resultados:
                resultado_formatado = "\n".join([str(resultado) for resultado in resultados])  # Formata os resultados
                return resultado_formatado
            else:
                return f"Nenhum dado encontrado para a nota fiscal {consulta['filtro']}."
        else:
            return "Pergunta não compreendida."


# Teste do Executor
if __name__ == "__main__":
    executor = AgenteExecutor()
    pergunta_teste = "Quais os itens vendidos na nota fiscal 3482?"
    resposta = executor.executar_pipeline(pergunta_teste)
    print(f"Resultado Final:\n{resposta}")
