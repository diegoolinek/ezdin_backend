from flask import Blueprint

lessons_bp = Blueprint('lessons', __name__)

from . import routes