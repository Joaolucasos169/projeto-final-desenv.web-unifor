from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from .models import Usuario
from .database import db
from sqlalchemy.exc import IntegrityError
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

# Rota para a página inicial (login)
@auth_bp.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# Rota para exibir a página de registro
@auth_bp.route('/register.html', methods=['GET'])
def register_page():
    return render_template('register.html')

# Rota para processar o registro
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    nome = data.get('nome')
    sobrenome = data.get('sobrenome')
    email = data.get('email')
    senha = data.get('senha')
    data_nascimento_str = data.get('dataNascimento')

    if not all([nome, sobrenome, email, senha, data_nascimento_str]):
        return jsonify({"error": "Todos os campos são obrigatórios"}), 400

    try:
        data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date()
        new_user = Usuario(nome=nome, sobrenome=sobrenome, email=email, senha=senha, data_nascimento=data_nascimento)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Usuário cadastrado com sucesso", "redirect": "/"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "E-mail já cadastrado"}), 409
    except ValueError:
        return jsonify({"error": "Data de nascimento inválida"}), 400
    except Exception as e:
        print(e)  # Log para ajudar na depuração
        return jsonify({"error": "Erro ao cadastrar. Tente novamente mais tarde."}), 500
