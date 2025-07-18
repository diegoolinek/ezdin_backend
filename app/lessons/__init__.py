# app/lessons/__init__.py
from flask import Blueprint

lessons_bp = Blueprint('lessons', __name__)

from . import routes # Importa as rotas para registrá-las no blueprint