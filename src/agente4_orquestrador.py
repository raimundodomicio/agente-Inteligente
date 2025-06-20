from agente1_descompactador import AgenteDescompactador
from agente2_indexador import AgenteIndexador
from agente3_interpretador import AgenteInterpretador

class AgenteOrquestrador:
    def __init__(self, caminho_zip="202401_NFs.zip"): #Inicializa os agentes e prepara os dados
        self.descompactador = AgenteDescompactador(caminho_zip)
        self.indexador = AgenteIndexador()
        self.interpretador = AgenteInterpretador()

        # Etapa opcional: descompactar os dados (somente se necessário)
        self.descompactador.descompactar_zip()

        # Carrega e indexa os dados (se ainda não carregados)
        self.indexador.carregar_dados()

    def executar_pergunta(self, pergunta): #Executa o ciclo de compreensão e resposta
        consulta = self.interpretador.interpretar_pergunta(pergunta)

        if not consulta:
            return "Não entendi sua pergunta. Pode reformular a pergunta?"

        campo, filtro = consulta["campo"], consulta["filtro"]
        resultados = self.indexador.buscar(filtro)

        if not resultados:
            return f"Nenhum dado encontrado para a nota fiscal {filtro}."

        return self.gerar_resposta(campo, filtro, resultados)

    def gerar_resposta(self, campo, filtro, registros): #Gera uma resposta em linguagem natural baseada nos dados
        if campo == "cliente":
            cliente = registros[0].get("cliente", "Cliente não identificado")
            return f"O cliente da nota fiscal {filtro} é: {cliente}."

        elif campo == "produto":
            produtos = [r.get("descricao_produto", "produto não identificado") for r in registros]
            lista = "\n- " + "\n- ".join(produtos)
            return f"Itens vendidos na nota fiscal {filtro}:{lista}"

        elif campo == "valor":
            valor = registros[0].get("valor_total") or registros[0].get("valor", None)
            if valor:
                return f"O valor total da nota fiscal {filtro} é R$ {valor:.2f}."
            return f"Valor da nota {filtro} não localizado."

        else:
            return f"Ainda não sei como responder perguntas sobre '{campo}'."

# Teste local
if __name__ == "__main__":
    agente = AgenteOrquestrador()
    perguntas = [
        "Quem foi o comprador na nota fiscal 5183?",
        "Qual o total da nota fiscal 369180?",
        "Quais os produtos na nota fiscal 17055?"
    ]

    for pergunta in perguntas:
        resposta = agente.executar_pergunta(pergunta)
        print(f"\nPergunta: {pergunta}\nResposta: {resposta}")
