import os
from flask import Flask, render_template, request, redirect, url_for
import psycopg2 # Importa a nova biblioteca
from datetime import datetime

app = Flask(__name__)

# Pega a URL do banco de dados da variável de ambiente configurada no Render
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db_connection():
    # Usa psycopg2 para conectar ao PostgreSQL
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# A função init_db agora usa a conexão do PostgreSQL
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    # O SQL para criar a tabela é o mesmo
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profissionais_pcd (
            id SERIAL PRIMARY KEY,
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
    cursor.close()
    conn.close()
    print("Tabela 'profissionais_pcd' verificada/criada no PostgreSQL.")

# O resto do seu código permanece praticamente o mesmo
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

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
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO profissionais_pcd (nome_completo, email, telefone, formacao, experiencias, habilidades, tipo_deficiencia, necessidades_especificas, data_cadastro)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (nome, email, telefone, formacao, experiencias, habilidades, tipo_deficiencia, necessidades_especificas, data_cadastro))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('sucesso'))

@app.route('/sucesso')
def sucesso():
    return render_template('sucesso.html')

if __name__ == '__main__':
    # Não precisamos mais chamar init_db() aqui, faremos isso de outra forma
    app.run(debug=True)
if __name__ == '__main__':
    init_db()

    app.run(debug=True)
