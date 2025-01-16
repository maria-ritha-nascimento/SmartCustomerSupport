from flask import Flask
from flask_cors import CORS
from app.models.database import init_db
from app.api.routes import api_bp
from flask_swagger_ui import get_swaggerui_blueprint

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'supersecretkey'

    # Inicializar banco de dados
    init_db(app)

    # Configurar CORS
    CORS(app)

    # Registrar blueprints
    app.register_blueprint(api_bp)

    # Configurar Swagger
    SWAGGER_URL = '/docs'
    API_URL = '/static/swagger.json'
    swaggerui_bp = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
    app.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)

    return app
