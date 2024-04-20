from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# Importando os elementos definidos no modelo
from model.base import Base
from model.comentario import Comentario
from model.produto import Produto

db_path = "database/"
if not os.path.exists(db_path): # Verifica se o diretorio não existe
    os.makedirs(db_path) # Cria o diretorio, caso não exista


db_url = 'sqlite:///%s/db.sqlite3' % db_path # Url de acesso ao banco

engine = create_engine(db_url, echo=False) # Cria a engine de conexão com o bd

Session = sessionmaker(bind=engine) # Instancia um criador de seção com o banco

if not database_exists(engine.url): # Cria o banco se ele não existir
    create_database(engine.url)

Base.metadata.create_all(engine) # Cria as tabelas do banco, caso não existam