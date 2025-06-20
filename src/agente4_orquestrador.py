from agente1_descompactador import AgenteDescompactador
from agente2_indexador import AgenteIndexador
from agente3_interpretador import AgenteInterpretador

class AgenteOrquestrador:
    def __init__(self, caminho_zip="202401_NFs.zip"): #Inicializa os agentes e carrega os dados
        self.descompactador = AgenteDescompactador(caminho_zip)
        self.indexador = AgenteIndexador()
        self.interpretador = AgenteInterpretador()

        self.descompactador.descompactar_zip()
        self.indexador.carregar_dados()

    def executar_pergunta(self, pergunta):#Executa o ciclo completo: interpretar -> buscar -> responder
        consulta = self.interpretador.interpretar_pergunta(pergunta)

        if not consulta:
            return "Ops! Não entendi a pergunta. Pode reformular?"

        campo = consulta["campo"]
        filtro = consulta["filtro"]

        registros = self.indexador.buscar_por_numero_nf(filtro)

        if not registros:
            return f"Nenhum dado encontrado para a nota fiscal {filtro}."

        return self.gerar_resposta(campo, filtro, registros)

    def gerar_resposta(self, campo, filtro, registros):#Gera resposta em linguagem natural baseada no campo solicitado
        # Cliente (destinatário)
        if campo == "cliente":
            cliente = registros[0].get("NOME DESTINATÁRIO", "Cliente não identificado")
            return f"O cliente da nota fiscal {filtro} é: {cliente}."

        # Valor total da nota
        elif campo == "valor":
            valor = registros[0].get("VALOR NOTA FISCAL") or registros[0].get("VALOR TOTAL")
            if valor:
                return f"O valor total da nota fiscal {filtro} é R$ {float(valor):.2f}."
            return f"Valor da nota fiscal {filtro} não localizado nos registros."

        # Produtos vendidos
        elif campo == "produto":
            produtos = [
                r.get("DESCRIÇÃO DO PRODUTO/SERVIÇO")
                for r in registros
                if pd.notnull(r.get("DESCRIÇÃO DO PRODUTO/SERVIÇO"))
            ]
            if produtos:
                lista = "\n- " + "\n- ".join(set(produtos))
                return f"Itens da nota fiscal {filtro}:{lista}"
            return f"Não foram encontrados itens na nota fiscal {filtro}."

        # Caso o campo não esteja mapeado
        else:
            return f"Ainda não sei como responder perguntas sobre '{campo}'."

# Teste local do Agente 4
if __name__ == "__main__":
    agente = AgenteOrquestrador()
    perguntas = [
        "Quem foi o comprador na nota fiscal 5183?",
        "Qual o total da nota fiscal 369180?",
        "Quais os produtos na nota fiscal 17055?"
    ]

    for pergunta in perguntas:
        resposta = agente.executar_pergunta(pergunta)
        print(f"\n🧾 Pergunta: {pergunta}\n📎 Resposta: {resposta}")
