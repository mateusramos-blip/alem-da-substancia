from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__, template_folder=".", static_folder=".")
CORS(app)  # Permite que o seu index.html converse com o Python sem bloqueios de segurança

DATABASE = 'data/database.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        # Cria a tabela de acessos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS acessos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total INTEGER DEFAULT 0
            )
        ''')
        # Cria a tabela de depoimentos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS depoimentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                texto TEXT
            )
        ''')
        
        # Garante que existe pelo menos uma linha para o contador iniciar
        cursor.execute("SELECT COUNT(*) FROM acessos")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO acessos (total) VALUES (179)") # Começa com o valor base do seu site
        conn.commit()

# Rota para atualizar e retornar as visitas
@app.route('/api/visita', methods=['POST'])
def registrar_visita():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE acessos SET total = total + 1 WHERE id = 1")
        cursor.execute("SELECT total FROM acessos WHERE id = 1")
        total = cursor.fetchone()[0]
        conn.commit()
    return jsonify({"total_visitantes": total})

# Rota para listar os depoimentos
@app.route('/api/depoimentos', methods=['GET'])
def listar_depoimentos():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT nome, texto FROM depoimentos ORDER BY id DESC")
        linhas = cursor.fetchall()
    
    depoimentos = [{"nome": l[0], "texto": l[1]} for l in linhas]
    return jsonify(depoimentos)

# Rota para salvar um novo depoimento
@app.route('/api/depoimentos', methods=['POST'])
def salvar_depoimento():
    dados = request.get_json()
    nome = dados.get('nome', 'Anônimo')
    texto = dados.get('texto', '')
    
    if not texto:
        return jsonify({"erro": "O texto do depoimento é obrigatório"}), 400
        
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO depoimentos (nome, texto) VALUES (?, ?)", (nome, texto))
        conn.commit()
        
    return jsonify({"status": "sucesso"}), 201

import os

@app.route('/')
def index():
    import flask
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return flask.send_from_directory(base_dir, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    import flask
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return flask.send_from_directory(base_dir, filename)

if __name__ == '__main__':
    init_db()
    print("Servidor do Projeto Além da Substância rodando com sucesso!")
    app.run(debug=True, port=5000)