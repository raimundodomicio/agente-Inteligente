import re
import nltk
import spacy
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TreebankWordTokenizer
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine

# Inicialização dos recursos NLP
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)
spacy_model = spacy.load("pt_core_news_sm")

# Modelo de embeddings
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

class AgenteInterpretador:
    def __init__(self):
        self.categorias = {
            "produto": ["produto", "item", "mercadoria", "itens", "produtos", "bens"],
            "valor": ["valor", "preço", "total", "custo", "gasto"],
            "cliente": ["cliente", "comprador", "destinatário", "consumidor", "empresa"],
            #"nota fiscal": ["nota", "nf", "documento", "registro", "nota fiscal", "nota fiscal eletrônica"],
        }
        self.lemmatizer = WordNetLemmatizer()
        self.tokenizer = TreebankWordTokenizer()

    def interpretar_pergunta(self, pergunta):
        pergunta = pergunta.lower()
        tokens = self.tokenizer.tokenize(pergunta)
        lemas = [self.lemmatizer.lemmatize(token) for token in tokens]
        frase_embedding = embedding_model.encode(" ".join(lemas))

        resultado = {
            "tipo": None,
            "campo": None,
            "operacao": None,
            "filtro": None
        }

        # Detectar número de nota (se houver)
        match = re.search(r'\b\d{3,}\b', pergunta)
        if match:
            resultado["filtro"] = match.group()
            resultado["tipo"] = "consulta_por_nf"
        else:
            resultado["tipo"] = "consulta_global"

        # Mapeia categoria mais próxima semanticamente
        melhor_categoria = None
        menor_distancia = float("inf")
        for categoria, palavras_chave in self.categorias.items():
            for palavra in palavras_chave:
                palavra_embedding = embedding_model.encode(palavra)
                distancia = cosine(frase_embedding, palavra_embedding)
                if distancia < menor_distancia:
                    menor_distancia = distancia
                    melhor_categoria = categoria

        resultado["campo"] = melhor_categoria

        # Detectar operações agregadas ou estatísticas
        if resultado["tipo"] == "consulta_global":
            if "maior" in pergunta or "mais alto" in pergunta:
                resultado["operacao"] = "max"
            elif "menor" in pergunta or "mais baixo" in pergunta:
                resultado["operacao"] = "min"
            elif "média" in pergunta and "cliente" in pergunta:
                resultado["operacao"] = "media_por_cliente"
            elif "média" in pergunta or "médio" in pergunta:
                resultado["operacao"] = "media"
            elif "mais vendido" in pergunta or "mais vendidos" in pergunta or "mais comprados" in pergunta:
                resultado["operacao"] = "mais_frequente"
            elif "mais aparece" in pergunta or "repetido" in pergunta or "comprador mais frequente" in pergunta:
                resultado["operacao"] = "mais_frequente"

            # Captura nome de cliente (tentativa simples)
            if resultado["operacao"] == "media_por_cliente":
                doc = spacy_model(pergunta)
                nomes = [ent.text for ent in doc.ents if ent.label_ == "PER"]
                if nomes:
                    resultado["filtro"] = nomes[0]

        return resultado if resultado["campo"] else None


# Teste do Agente
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
