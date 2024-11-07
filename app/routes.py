from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash
from .models import Usuario, Agendamento
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
    return render_template('home.html')

# Rota para processar o logout
@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)  # Remove o usuário da sessão
    return redirect(url_for('auth.home'))  # Redireciona para a página de login

# Rota para a tela de agendamento
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

# Rota para exibir a página de reimpressão de agendamento
@auth_bp.route('/reimprimir_agendamento', methods=['GET'])
def reimprimir_agendamento_page():
    return render_template('reimprimir_agendamento.html')

# Rota para processar a reimpressão de agendamento
@auth_bp.route('/reimprimir_agendamento', methods=['POST'])
def reimprimir_agendamento():
    agendamento_id = request.form.get('agendamento_id')  # Captura o ID do agendamento
    if not agendamento_id:
        flash("Erro: ID do agendamento não foi fornecido.", "error")
        return redirect(url_for('auth.reimprimir_agendamento_page'))
    
    # Procura o agendamento no banco de dados
    agendamento = Agendamento.query.get(agendamento_id)
    
    if not agendamento:
        # Caso o agendamento não seja encontrado
        flash("Agendamento não encontrado.", "error")
        return render_template('reimprimir_agendamento.html')
    
    # Caso o agendamento seja encontrado, redireciona para a página de detalhes
    return redirect(url_for('auth.detalhes_agendamento', agendamento_id=agendamento_id))

# Rota para exibir a página de cancelamento de agendamento
@auth_bp.route('/cancelar_agendamento', methods=['GET'])
def cancelar_agendamento_page():
    return render_template('cancelar_agendamento.html')

# Rota POST para cancelar o agendamento
@auth_bp.route('/cancelar_agendamento', methods=['POST'])
def cancelar_agendamento():
    agendamento_id = request.form.get('agendamento_id')
    
    # Procura o agendamento no banco de dados
    agendamento = Agendamento.query.get(agendamento_id)
    
    if agendamento:
        # Realiza o cancelamento, neste caso excluindo o agendamento
        db.session.delete(agendamento)
        db.session.commit()
        
        # Mensagem de sucesso
        flash("Agendamento cancelado com sucesso!", "success")
    else:
        # Mensagem de erro se o agendamento não for encontrado
        flash("Agendamento não encontrado.", "error")
    
    # Renderiza a mesma página de cancelamento com a mensagem de flash
    return render_template('cancelar_agendamento.html')
