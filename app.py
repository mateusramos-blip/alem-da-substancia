import os
import sqlite3
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATABASE = os.path.join(DATA_DIR, "database.db")

app = Flask(__name__, template_folder=BASE_DIR, static_folder=BASE_DIR)
CORS(app)


def ensure_data_directory() -> None:
    """Create the local data directory when it is missing."""
    os.makedirs(DATA_DIR, exist_ok=True)


def get_db_connection() -> sqlite3.Connection:
    """Open a new SQLite connection for each request."""
    return sqlite3.connect(DATABASE)


def init_db() -> None:
    """Initialize database tables and default values."""
    ensure_data_directory()

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS acessos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total INTEGER DEFAULT 0
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS depoimentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                texto TEXT
            )
            """
        )
        cursor.execute("SELECT COUNT(*) FROM acessos")
        result = cursor.fetchone()

        if not result or result[0] == 0:
            cursor.execute("INSERT INTO acessos (total) VALUES (179)")

        conn.commit()


init_db()


@app.route("/api/visita", methods=["POST"])
def registrar_visita() -> jsonify:
    """Increment the visitor counter and return the updated total."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE acessos SET total = total + 1 WHERE id = 1")
        cursor.execute("SELECT total FROM acessos WHERE id = 1")
        total = cursor.fetchone()[0]
        conn.commit()

    return jsonify({"total_visitantes": total})


@app.route("/api/depoimentos", methods=["GET"])
def listar_depoimentos() -> jsonify:
    """Return all stored depoimentos in descending order."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT nome, texto FROM depoimentos ORDER BY id DESC")
        rows = cursor.fetchall()

    depoimentos = [{"nome": row[0], "texto": row[1]} for row in rows]
    return jsonify(depoimentos)


@app.route("/api/depoimentos", methods=["POST"])
def salvar_depoimento() -> tuple:
    """Save a new depoimento sent by the frontend."""
    payload = request.get_json(silent=True) or {}
    nome = payload.get("nome", "Anônimo")
    texto = payload.get("texto", "")

    if not texto.strip():
        return jsonify({"erro": "O texto do depoimento é obrigatório"}), 400

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO depoimentos (nome, texto) VALUES (?, ?)",
            (nome.strip() or "Anônimo", texto.strip()),
        )
        conn.commit()

    return jsonify({"status": "sucesso"}), 201


@app.route("/")
def index() -> str:
    """Serve the main HTML page."""
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/<path:filename>")
def serve_static(filename: str):
    """Serve static files while protecting API routes."""
    if filename.startswith("api/"):
        return jsonify({"erro": "Rota nao encontrada"}), 404

    return send_from_directory(BASE_DIR, filename)


def main() -> None:
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
