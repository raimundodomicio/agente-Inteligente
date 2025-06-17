import re
import nltk
import spacy
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TreebankWordTokenizer
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine

# Inicialização do NLTK e spaCy
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)
#spacy_model = spacy.load("en_core_web_sm")  # Para inglês
spacy_model = spacy.load("pt_core_news_sm")  # Modelo spaCy para português

# Modelo de embeddings para similaridade semântica
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

class AgenteInterpretador:
    def __init__(self):
        self.categorias = {
            "produto": ["produto", "item", "mercadoria", "itens"],
            "valor": ["valor", "preço", "total", "custo"],
            "cliente": ["cliente", "comprador", "destinatário"],
            "nota fiscal": ["nota", "nf", "documento"]
        }
        self.lemmatizer = WordNetLemmatizer()
        self.tokenizer = TreebankWordTokenizer()

    def interpretar_pergunta(self, pergunta):
        pergunta = pergunta.lower()
        tokens = self.tokenizer.tokenize(pergunta)
        lemas = [self.lemmatizer.lemmatize(token) for token in tokens]

        resultado = {"campo": None, "filtro": None}

        # Vetorização da pergunta
        frase_embedding = embedding_model.encode(" ".join(lemas))

        # Comparar com categorias usando distância de cosseno
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

        # Extrai número de nota fiscal
        match = re.search(r'\b\d{3,}\b', pergunta)
        if match:
            resultado["filtro"] = match.group()

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
