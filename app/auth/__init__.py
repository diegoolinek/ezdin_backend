# app/auth/__init__.py
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from . import routes # Importa as rotas para registrá-las no blueprint