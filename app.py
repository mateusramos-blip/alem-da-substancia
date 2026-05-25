import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__, template_folder=".", static_folder=".")
CORS(app)  

DATABASE = 'data/database.db'

# Garante que a pasta 'data' existe antes de mexer no banco
os.makedirs('data', exist_ok=True)

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS acessos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total INTEGER DEFAULT 0
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS depoimentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                texto TEXT
            )
        ''')
        
        cursor.execute("SELECT COUNT(*) FROM acessos")
        # CORREÇÃO AQUI: adicionado o [0] para ler o número corretamente
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO acessos (total) VALUES (179)") 
        conn.commit()

# Inicializa o banco de dados com segurança
init_db()

# ... O RESTO DO SEU CÓDIGO DAQUI PARA BAIXO CONTINUA IGUAL ...
