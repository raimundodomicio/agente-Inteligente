
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.agente3_interpretador import AgenteInterpretador

if __name__ == "__main__":
    agente = AgenteInterpretador()
    perguntas = [
        "Qual o total da nota fiscal 2525?",
        "Quais os itens vendidos na nota fiscal 3482?",
        "Quem foi o comprador na NF 1975?"
    ]

    for pergunta in perguntas:
        consulta_interpretada = agente.interpretar_pergunta(pergunta)
        print(f"Pergunta: {pergunta}")
        print(f"Consulta gerada: {consulta_interpretada}\n")
