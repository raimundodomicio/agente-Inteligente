

import pandas as pd
import json
from src.agente1_descompactador import AgenteDescompactador
from src.agente2_indexador import AgenteIndexador
from src.agente3_interpretador import AgenteInterpretador

class AgenteOrquestrador:
    def __init__(self, caminho_zip="../202401_NFs.zip"):
        print("Iniciando o Agente Orquestrador...")
        self.descompactador = AgenteDescompactador(caminho_zip, pasta_destino="./data")
        self.indexador = AgenteIndexador(pasta_dados="./data")
        self.interpretador = AgenteInterpretador()

        print("Executando tarefas de inicialização...")
        self.descompactador.descompactar_zip()
        self.indexador.carregar_dados()
        print("Orquestrador pronto para receber perguntas.")

    def executar_pergunta(self, pergunta):
        """
        Executa o ciclo completo: interpretar -> buscar -> responder.
        """
        resposta_interpretador = self.interpretador.interpretar_pergunta(pergunta)

        # Se a resposta do interpretador for um dicionário (saudação ou erro direto)
        if isinstance(resposta_interpretador, dict):
            if resposta_interpretador.get("tipo") == "saudacao":
                return "Olá! Como posso ajudar com as notas fiscais?"
            elif resposta_interpretador.get("tipo") == "erro_interpretacao":
                return "Desculpe, tive um problema ao interpretar sua pergunta. Pode tentar reformular?"
            # Fallback para outros tipos de dicionário inesperados
            else:
                return "Não entendi sua pergunta. Pode ser mais específico?"

        # Se a resposta do interpretador for uma string (JSON)
        try:
            consulta = json.loads(resposta_interpretador)
        except (json.JSONDecodeError, TypeError):
            # Se a resposta não for um JSON válido, tratamos como uma consulta global desconhecida
            consulta = {"tipo": "consulta_global", "campo": "desconhecido", "filtro": None}

        tipo = consulta.get("tipo")
        campo = consulta.get("campo")
        filtro = consulta.get("filtro")

        # Se o modelo não souber o que fazer, use a busca semântica como padrão
        if campo == "desconhecido":
            tipo = "consulta_global"

        if tipo == "consulta_por_nf" and filtro:
            registros = self.indexador.buscar_por_numero_nf(filtro)
            if not registros:
                return f"Nenhum dado encontrado para a nota fiscal {filtro}."
            return self.gerar_resposta_nf(campo, filtro, registros)
        
        elif tipo == "consulta_global":
            resultados = self.indexador.buscar_semantico(pergunta)
            if not resultados:
                return f"Não encontrei resultados para a busca: '{pergunta}'"
            
            resposta_formatada = "Encontrei os seguintes registros relacionados:\n\n" + "\n---\n".join(resultados)
            return resposta_formatada

        else:
            return "Não entendi o que você precisa. Tente perguntar de outra forma."

    def gerar_resposta_nf(self, campo, filtro, registros):
        """
        Gera uma resposta em linguagem natural para consultas de NF específicas.
        """
        if campo == "cliente":
            cliente = registros[0].get("NOME DESTINATÁRIO", "não identificado")
            return f"O cliente da nota fiscal {filtro} é: {cliente}."

        elif campo == "valor":
            valor = registros[0].get("VALOR NOTA FISCAL") or registros[0].get("VALOR TOTAL")
            if valor:
                return f"O valor total da nota fiscal {filtro} é R$ {float(valor):.2f}."
            return f"Não localizei o valor da nota fiscal {filtro}."

        elif campo == "produto":
            produtos = [r.get("DESCRIÇÃO DO PRODUTO/SERVIÇO") for r in registros if pd.notnull(r.get("DESCRIÇÃO DO PRODUTO/SERVIÇO"))]
            if produtos:
                lista_formatada = "\n- " + "\n- ".join(set(produtos))
                return f"Os itens da nota fiscal {filtro} são:{lista_formatada}"
            return f"Não encontrei itens na nota fiscal {filtro}."

        else:
            info = registros[0]
            return f"Encontrei a nota fiscal {filtro}. Aqui estão os detalhes principais: \nCliente: {info.get('NOME DESTINATÁRIO', 'N/A')} \nValor: R$ {info.get('VALOR NOTA FISCAL', 'N/A')}"
