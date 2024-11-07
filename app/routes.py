from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from .models import Usuario
from .database import db
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from .models import Usuario, Agendamento
from .models import Agendamento
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

# Rota para processar o login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('password')

    user = Usuario.query.filter_by(email=email).first()

    if user and user.check_password(senha):
        session['user_id'] = user.id  # Armazena o ID do usuário na sessão
        return jsonify({"message": "Login bem-sucedido"}), 200
    else:
        return jsonify({"error": "E-mail ou senha incorretos"}), 401

# Rota para a tela principal
@auth_bp.route('/home', methods=['GET'])
def main_page():
    return render_template('home.html')  # Certifique-se de que você tem um arquivo home.html

@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)  # Remove o usuário da sessão
    return redirect(url_for('auth.home'))  # Redireciona para a página de login

# Rota gerar senha
@auth_bp.route('/agendamento')
def agendamento():
    return render_template('agendamento.html')


# Rota para processar o agendamento
@auth_bp.route('/agendamento', methods=['POST'])
def process_agendamento():
    local = request.form['local']
    setor = request.form['setor']
    servico = request.form['servico']
    data = request.form['data']
    horario = request.form['horario']
    nome = request.form['nome']
    cpf = request.form['cpf']
    email = request.form['email']
    telefone = request.form['telefone']
    
    # Combinar data e horário em um único datetime
    data_hora_str = f"{data} {horario}"
    data_agendamento = datetime.strptime(data_hora_str, '%Y-%m-%d %H:%M')

    # Verificar se o usuário está logado para associar ao agendamento
    usuario_id = 1  # Substitua isso com a lógica para obter o ID do usuário logado

    # Criar o agendamento
    novo_agendamento = Agendamento(
        usuario_id=usuario_id,
        local=local,
        setor=setor,
        servico=servico,
        nome=nome,
        cpf=cpf,
        email=email,
        telefone=telefone,
        data_agendamento=data_agendamento,
        descricao="Agendamento realizado com sucesso"
    )

    db.session.add(novo_agendamento)
    db.session.commit()

    # Redireciona para a página de detalhes do agendamento
    return redirect(url_for('auth.detalhes_agendamento', agendamento_id=novo_agendamento.id))

# Rota para exibir os detalhes do agendamento
@auth_bp.route('/detalhes_agendamento/<int:agendamento_id>', methods=['GET'])
def detalhes_agendamento(agendamento_id):
    agendamento = Agendamento.query.get_or_404(agendamento_id)
    return render_template('detalhes_agendamento.html', agendamento=agendamento)
