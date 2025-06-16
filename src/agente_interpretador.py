import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TreebankWordTokenizer


# Inicialização do NLTK
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)

class AgenteInterpretador:
    def __init__(self):
        self.padroes_perguntas = {
            "produto": ["produto", "item", "mercadoria"],
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

        for categoria, palavras_chave in self.padroes_perguntas.items():
            if any(lemma in palavras_chave for lemma in lemas):
                resultado["campo"] = categoria
                break

        match = re.search(r'\b\d{3,}\b', pergunta)
        if match:
            resultado["filtro"] = match.group()

        return resultado if resultado["campo"] else None

# Teste do Agente
if __name__ == "__main__":
    agente = AgenteInterpretador()
    perguntas = [
        "Qual o valor total da nota fiscal 2525?",
        "Quais os itens vendidos na nota fiscal 3482?",
        "Quem foi o comprador na NF 1975?"
    ]

    for pergunta in perguntas:
        consulta_interpretada = agente.interpretar_pergunta(pergunta)
        print(f"Pergunta: {pergunta}")
        print(f"Consulta gerada: {consulta_interpretada}\n")
