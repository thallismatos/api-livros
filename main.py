from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Conectar ao banco de dados e criar a tabela se não existir
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS LIVROS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            categoria TEXT NOT NULL,
            autor TEXT NOT NULL,
            imagem_url TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


init_db()

# Página inicial
@app.route('/')
def home():
    return "API de livros rodando no render"

# Rota para cadastrar um livro
@app.route('/doar', methods=['POST'])
def doar():
    if request.content_type != 'application/json':
        return jsonify({"error": "Content-Type must be application/json"}), 415

    data = request.get_json()

    if not data or not all(k in data for k in ("titulo", "categoria", "autor", "imagem_url")):
        return jsonify({"error": "Dados inválidos ou incompletos"}), 400

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO LIVROS (titulo, categoria, autor, imagem_url) VALUES (?, ?, ?, ?)",
                   (data["titulo"], data["categoria"], data["autor"], data["imagem_url"]))
    conn.commit()
    conn.close()

    return jsonify({"message": "Livro cadastrado com sucesso!"}), 201

# Rota para listar os livros
@app.route('/livros', methods=['GET'])
def listar_livros():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM LIVROS")
    livros = cursor.fetchall()
    conn.close()

    livros_json = [{"id": livro[0], "titulo": livro[1], "categoria": livro[2],
                    "autor": livro[3], "imagem_url": livro[4]} for livro in livros]

    return jsonify(livros_json)


if __name__ == '__main__':
    from os import environ
    port = int(environ.get('PORT', 10000)) 
    app.run(host='0.0.0.0', port=port, debug=False)
