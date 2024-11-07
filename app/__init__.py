from flask import Flask
from .config import Config
from .database import db
from .routes import auth_bp
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__, static_folder="static")
    app.config.from_object(Config)

    # Inicializar o banco de dados
    db.init_app(app)

    # Inicializar o Flask-Migrate
    migrate = Migrate(app, db)

    # Registrar blueprints para organizar as rotas
    app.register_blueprint(auth_bp)

    return app
