import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__, template_folder=".", static_folder=".")
CORS(app)  # Permite que o seu index.html converse com o Python sem bloqueios de segurança

DATABASE = 'data/database.db'

# === CORREÇÃO 1: Garante que a pasta 'data' existe antes de mexer no banco ===
os.makedirs('data', exist_ok=True)

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

# === CORREÇÃO 2: Executa a criação das tabelas assim que o app inicia ===
init_db()

# ... O RESTO DO SEU CÓDIGO DAQUI PARA BAIXO CONTINUA EXATAMENTE IGUAL ...
