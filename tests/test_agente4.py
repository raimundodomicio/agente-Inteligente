

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.agente4_orquestrador import AgenteOrquestrador

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

