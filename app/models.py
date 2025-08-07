from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False) # Email do usuário
    password_hash = db.Column(db.String(256), nullable=False)
    points = db.Column(db.Integer, default=0)
    name = db.Column(db.String(100), nullable=True) # Nome completo ou apelido, opcional
    bio = db.Column(db.Text, nullable=True)
    joined_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False) # Data de cadastro
    avatar_url = db.Column(db.String(256), nullable=True) # URL para a imagem do avatar, opcional
    is_admin = db.Column(db.Boolean, default=False) # Campo para determinar se é admin

    progresses = db.relationship('UserProgress', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    challenge_question = db.Column(db.String(256), nullable=False)
    # Para múltipla escolha
    option_a = db.Column(db.String(256), nullable=True)
    option_b = db.Column(db.String(256), nullable=True)  
    option_c = db.Column(db.String(256), nullable=True)
    option_d = db.Column(db.String(256), nullable=True)
    correct_option = db.Column(db.String(1), nullable=False)  # 'a', 'b', 'c', 'd'
    explanation = db.Column(db.Text, nullable=True)
    points_awarded = db.Column(db.Integer, default=10)
    order_index = db.Column(db.Integer, unique=True, nullable=False)

    progresses = db.relationship('UserProgress', backref='lesson', lazy='dynamic')

    def __repr__(self):
        return f'<Lesson {self.title}>'

class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('user_id', 'lesson_id', name='_user_lesson_uc'),)

    def __repr__(self):
        return f'<UserProgress User:{self.user_id} Lesson:{self.lesson_id} Completed:{self.is_completed}>'