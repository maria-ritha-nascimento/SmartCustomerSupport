from flask import Flask
from app.models.database import init_db
from app.api.routes import api_bp


def create_app():
    app = Flask(__name__)

    # Configurações do app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'supersecretkey'  # Chave secreta para autenticação

    # Inicializar banco de dados
    init_db(app)

    # Registrar blueprints
    app.register_blueprint(api_bp)

    return app