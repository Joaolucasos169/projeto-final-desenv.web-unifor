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
    local = db.Column(db.String(50), nullable=False)
    setor = db.Column(db.String(50), nullable=False)
    servico = db.Column(db.String(50), nullable=False)
    data_agendamento = db.Column(db.DateTime, nullable=False)  # Ajustando para um único campo DateTime

    # Dados do usuário
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(15), nullable=False)

    def __init__(self, usuario_id, local, setor, servico, nome, cpf, email, telefone, data_agendamento, descricao=None):
        self.usuario_id = usuario_id
        self.local = local
        self.setor = setor
        self.servico = servico
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.telefone = telefone
        self.data_agendamento = data_agendamento
        