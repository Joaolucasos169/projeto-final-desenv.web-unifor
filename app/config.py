import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'minha_chave_secreta')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://usuario:senha@localhost:5432/nome_do_banco')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
