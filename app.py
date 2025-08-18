import os
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DATABASE):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE profissionais_pcd (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_completo TEXT NOT NULL,
                email TEXT NOT NULL,
                telefone TEXT NOT NULL,
                formacao TEXT,
                experiencias TEXT,
                habilidades TEXT,
                tipo_deficiencia TEXT NOT NULL,
                necessidades_especificas TEXT,
                data_cadastro TIMESTAMP NOT NULL
            );
        ''')
        conn.commit()
        conn.close()
        print("Banco de dados inicializado.")

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para a página de cadastro
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

# Rota que processa os dados do formulário
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form['nome_completo']
    email = request.form['email']
    telefone = request.form['telefone']
    formacao = request.form['formacao']
    experiencias = request.form['experiencias']
    habilidades = request.form['habilidades']
    tipo_deficiencia = request.form['tipo_deficiencia']
    necessidades_especificas = request.form['necessidades_especificas']
    data_cadastro = datetime.now()

    conn = get_db_connection()
    conn.execute('''
        INSERT INTO profissionais_pcd (nome_completo, email, telefone, formacao, experiencias, habilidades, tipo_deficiencia, necessidades_especificas, data_cadastro)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nome, email, telefone, formacao, experiencias, habilidades, tipo_deficiencia, necessidades_especificas, data_cadastro))
    conn.commit()
    conn.close()

    return redirect(url_for('sucesso'))

@app.route('/sucesso')
def sucesso():
    return render_template('sucesso.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)