import os
import sqlite3
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATABASE = os.path.join(DATA_DIR, "database.db")

DATABASE_URL = os.environ.get("DATABASE_URL")

app = Flask(__name__, template_folder=BASE_DIR, static_folder=BASE_DIR)
CORS(app)


def ensure_data_directory() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)


def get_db_connection():
    if DATABASE_URL:
        import psycopg2
        return psycopg2.connect(DATABASE_URL)
    else:
        return sqlite3.connect(DATABASE)


def init_db() -> None:
    if not DATABASE_URL:
        ensure_data_directory()

    with get_db_connection() as conn:
        cursor = conn.cursor()

        if DATABASE_URL:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS acessos (
                    id SERIAL PRIMARY KEY,
                    total INTEGER DEFAULT 0
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS depoimentos (
                    id SERIAL PRIMARY KEY,
                    nome TEXT,
                    texto TEXT
                )
            """)
        else:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS acessos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    total INTEGER DEFAULT 0
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS depoimentos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT,
                    texto TEXT
                )
            """)

        cursor.execute("SELECT COUNT(*) FROM acessos")
        result = cursor.fetchone()

        if not result or result[0] == 0:
            if DATABASE_URL:
                cursor.execute("INSERT INTO acessos (total) VALUES (179)")
            else:
                cursor.execute("INSERT INTO acessos (id, total) VALUES (1, 179)")

        conn.commit()


init_db()


@app.route("/api/visita", methods=["POST"])
def registrar_visita():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE acessos SET total = total + 1 WHERE id = 1")
        cursor.execute("SELECT total FROM acessos WHERE id = 1")
        total = cursor.fetchone()[0]
        conn.commit()
    finally:
        conn.close()

    return jsonify({"total_visitantes": total})


@app.route("/api/depoimentos", methods=["GET"])
def listar_depoimentos():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT nome, texto FROM depoimentos ORDER BY id DESC")
        rows = cursor.fetchall()
    finally:
        conn.close()

    depoimentos = [{"nome": row[0], "texto": row[1]} for row in rows]
    return jsonify(depoimentos)


@app.route("/api/depoimentos", methods=["POST"])
def salvar_depoimento():
    payload = request.get_json(silent=True) or {}
    nome = payload.get("nome", "Anônimo")
    texto = payload.get("texto", "")

    if not texto.strip():
        return jsonify({"erro": "O texto do depoimento é obrigatório"}), 400

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        if DATABASE_URL:
            cursor.execute(
                "INSERT INTO depoimentos (nome, texto) VALUES (%s, %s)",
                (nome.strip() or "Anônimo", texto.strip()),
            )
        else:
            cursor.execute(
                "INSERT INTO depoimentos (nome, texto) VALUES (?, ?)",
                (nome.strip() or "Anônimo", texto.strip()),
            )
        conn.commit()
    finally:
        conn.close()

    return jsonify({"status": "sucesso"}), 201


@app.route("/")
def index() -> str:
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/<path:filename>")
def serve_static(filename: str):
    if filename.startswith("api/"):
        return jsonify({"erro": "Rota nao encontrada"}), 404
    return send_from_directory(BASE_DIR, filename)


def main() -> None:
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
