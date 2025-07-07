

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.agente2_indexador import AgenteIndexador

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

