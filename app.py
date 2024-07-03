from flask import Flask, jsonify
from sqlalchemy import create_engine
from urllib.parse import quote
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from sqlalchemy.orm import Session
from sqlalchemy.orm import Mapped

from flask import Flask, render_template, request, redirect, session, flash, url_for

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario("Bruno Divino", "BD", "alohomora")
usuario2 = Usuario("Camila Ferreira", "Mila", "paozinho")
usuario3 = Usuario("Guilherme Louro", "Cake", "python_eh_vida")

usuarios = { usuario1.nickname : usuario1,
             usuario2.nickname : usuario2,
             usuario3.nickname : usuario3 }

app = Flask(__name__)
app.secret_key = 'alura'

DB_PORT = 5431
DB_DATABASE = 'sysbib'
DB_USERNAME = 'postgres'
DB_PASSWORD = 'mysecretpassword'
DB_HOST = '127.0.0.1'

DATABASE_URI = f'postgresql://{DB_USERNAME}:{quote(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}'
engine = create_engine(DATABASE_URI)
session = Session(engine)

class Base(DeclarativeBase):
    pass

class Livros (Base):
    __tablename__ = "livros"
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(255))
    isbn: Mapped[str] = mapped_column(String(255))

app = Flask(__name__)

@app.route("/")
def hello_world():
    return session.query(Livros).all()[2].nome + " " + session.query(Livros).all()[2].isbn

@app.route("/")
def mostra_isbn():
    return session.query(Livros).all()[2].isbn

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

app.run(debug=True)
