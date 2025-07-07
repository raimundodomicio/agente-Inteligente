from flask import Flask, render_template, request, jsonify
import sys
import os

# Adiciona o diretório 'src' ao path para que possamos importar o orquestrador
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from agente4_orquestrador import AgenteOrquestrador

app = Flask(__name__)

# Variável global para o agente
agente = None

def initialize_agent():
    global agente
    print("Preparando o assistente... Por favor, aguarde.")
    agente = AgenteOrquestrador(caminho_zip="./202401_NFs.zip")
    print("Assistente pronto!")

# Inicializa o agente na primeira vez
initialize_agent()

@app.route('/')
def home():
    """
    Renderiza a página principal do chat.
    """
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    """
    Recebe a pergunta do usuário, processa com o agente e retorna a resposta.
    """
    data = request.get_json()
    pergunta = data.get("pergunta")

    if not pergunta:
        return jsonify({"resposta": "Por favor, digite uma pergunta."}), 400

    print(f"Recebida a pergunta: {pergunta}")
    resposta = agente.executar_pergunta(pergunta)
    print(f"Enviando resposta: {resposta}")
    
    return jsonify({"resposta": resposta})

@app.route('/clear_context', methods=['POST'])
def clear_context():
    """
    Reinicializa o agente para limpar o contexto da conversa.
    """
    initialize_agent()
    return jsonify({"status": "success", "message": "Contexto limpo com sucesso!"})

if __name__ == '__main__':
    # Inicia o servidor Flask
    app.run(debug=True, port=5000)