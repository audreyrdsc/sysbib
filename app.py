from flask import Flask, jsonify
from sqlalchemy import create_engine
from urllib.parse import quote
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from sqlalchemy.orm import Session
from sqlalchemy.orm import Mapped

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
    return session.query(Livros).all()[0].nome
