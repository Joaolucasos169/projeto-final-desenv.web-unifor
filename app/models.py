from .database import db 
from flask_bcrypt import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    sobrenome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)

    def __init__(self, nome, sobrenome, email, senha, data_nascimento):
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email
        self.senha_hash = generate_password_hash(senha).decode('utf-8')
        self.data_nascimento = data_nascimento

    def check_password(self, senha):
        return check_password_hash(self.senha_hash, senha)

class Agendamento(db.Model):
    __tablename__ = 'agendamentos'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    data_agendamento = db.Column(db.DateTime, nullable=False)
    descricao = db.Column(db.Text)

    def __init__(self, usuario_id, data_agendamento, descricao):
        self.usuario_id = usuario_id
        self.data_agendamento = data_agendamento
        self.descricao = descricao
