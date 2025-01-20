from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from app.models.database import init_db, db
from app.api.routes import api_bp
from flask_swagger_ui import get_swaggerui_blueprint
import logging

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'supersecretkey'

    # Configurar log para rastrear erros
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Inicializar banco de dados
    try:
        init_db(app)
        logger.info("Banco de dados inicializado com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao inicializar o banco de dados: {e}")

    # Configurar Flask-Migrate
    try:
        Migrate(app, db)
        logger.info("Flask-Migrate configurado com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao configurar Flask-Migrate: {e}")

    # Configurar CORS
    CORS(app)

    # Registrar blueprints
    try:
        app.register_blueprint(api_bp)
        logger.info("Blueprint de API registrado com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao registrar blueprint da API: {e}")

    # Configurar Swagger
    SWAGGER_URL = '/docs'
    API_URL = '/static/swagger.json'
    try:
        swaggerui_bp = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
        app.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)
        logger.info("Swagger configurado com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao configurar Swagger: {e}")

    return app
