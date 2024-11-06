from flask import Flask
from .config import Config
from .database import db
from .routes import auth_bp

def create_app():
    app = Flask(__name__, static_folder="static")
    app.config.from_object(Config)

    # Inicializar o banco de dados
    db.init_app(app)

    # Registrar blueprints para organizar as rotas
    app.register_blueprint(auth_bp)

    # Criar as tabelas do banco de dados
    with app.app_context():
        db.create_all()  # Cria todas as tabelas definidas nos modelos

    return app
