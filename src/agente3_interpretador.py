from transformers import pipeline
import json
import re

class AgenteInterpretador:
    def __init__(self, model="google/flan-t5-large"):
        """
        Inicializa o interpretador com um modelo de linguagem local da Hugging Face.
        """
        print("Inicializando o modelo de linguagem local. Isso pode levar alguns minutos...")
        self.nlp_pipeline = pipeline("text2text-generation", model=model)
        print("Modelo carregado com sucesso!")

    def interpretar_pergunta(self, pergunta):
        """
        Usa o modelo local para interpretar a pergunta e extrair informações estruturadas.
        """
        pergunta_lower = pergunta.lower().strip()

        # 1. Verificar saudações
        saudacoes = ["olá", "oi", "bom dia", "boa tarde", "boa noite", "e aí", "tudo bem"]
        if any(s in pergunta_lower for s in saudacoes):
            return {"tipo": "saudacao", "campo": None, "filtro": None}

        # 2. Prompt para o LLM - Pedindo um formato simples de chave:valor
        prompt = f'''
        Analise a pergunta abaixo e extraia as seguintes informações, uma por linha, no formato "chave: valor":
        - tipo: "consulta_por_nf" se a pergunta contiver um número de nota fiscal (ex: 1234, 56789), caso contrário "consulta_global".
        - campo: O principal campo de interesse na pergunta (ex: "cliente", "valor", "produto"). Se não for claro, use "desconhecido".
        - filtro: O número da nota fiscal, se presente, caso contrário null.

        Exemplos de saída:
        - Para "Qual o total da nota fiscal 1234?":
          tipo: consulta_por_nf
          campo: valor
          filtro: 1234
        - Para "Quem foi o comprador na NF 56789?":
          tipo: consulta_por_nf
          campo: cliente
          filtro: 56789
        - Para "Quais os produtos mais vendidos?":
          tipo: consulta_global
          campo: produto
          filtro: null
        - Para "Me diga algo sobre as notas fiscais":
          tipo: consulta_global
          campo: desconhecido
          filtro: null

        Pergunta: {pergunta}

        Saída:
        '''

        try:
            # Aumentar max_length para dar mais espaço ao modelo
            resultado = self.nlp_pipeline(prompt, max_length=200)
            raw_output = resultado[0]['generated_text']
            
            print(f"DEBUG: Saída bruta do modelo: {raw_output}") # Para depuração

            # Parsear a saída do modelo manualmente
            parsed_data = {}
            lines = raw_output.strip().split('\n')
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Converter 'null' string para None Python
                    if value.lower() == 'null':
                        value = None
                    
                    parsed_data[key] = value
            
            # Validar e retornar o dicionário
            if "tipo" in parsed_data and "campo" in parsed_data:
                return parsed_data
            else:
                raise ValueError("Saída do modelo incompleta ou malformada.")

        except Exception as e:
            print(f"Erro ao processar a pergunta com o modelo local: {e}")
            # Retorna uma estrutura de erro específica
            return {"tipo": "erro_interpretacao", "campo": None, "filtro": None}

# Teste local
if __name__ == '__main__':
    agente = AgenteInterpretador()
    perguntas = [
        "Qual o total da nota fiscal 2525?",
        "Quem foi o comprador na NF 1975?",
        "Qual o produto mais caro?",
        "Boa noite!",
        "Me diga algo sobre as notas fiscais",
        "Isso é um teste"
    ]

    for p in perguntas:
        interpretacao = agente.interpretador_pergunta(p)
        print(f"Pergunta: {p}")
        print(f"Interpretação: {interpretacao}\n")