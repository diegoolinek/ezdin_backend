import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
cors = CORS() 

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('instance.config.Config')

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Inicializa as extensões com o app
    db.init_app(app)
    login_manager.init_app(app)
    cors.init_app(app, supports_credentials=True) # Inicializa CORS

    # Configurações do Flask-Login
    login_manager.login_view = 'auth.login' # 'auth' é o nome do blueprint

    # Importa os modelos para que o SQLAlchemy os reconheça
    from app import models

    # Importa e registra os Blueprints
    from app.auth import auth_bp
    from app.lessons import lessons_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(lessons_bp, url_prefix='/api/lessons')

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(models.User, int(user_id))

    return app