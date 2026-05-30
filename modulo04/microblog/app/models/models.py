from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app.alquimias import db
# Importa o objeto login (LoginManager) inicializado em __init__.py
from app import login


class User(UserMixin, db.Model):
    """Modelo de usuário.

    Herda de UserMixin (Flask-Login), que fornece as implementações padrão de
    is_authenticated, is_active, is_anonymous e get_id() usadas internamente.
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))

    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def set_password(self, password):
        """Gera e armazena o hash da senha (nunca guardamos a senha pura)."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Confere se a senha informada corresponde ao hash armazenado."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Post(db.Model):
    """Publicação do microblog, associada a um usuário (author)."""
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(280))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<Post {self.body}>'


@login.user_loader
def load_user(id):
    """Função usada internamente pelo Flask-Login para recuperar o usuário
    atual a partir do id armazenado na sessão."""
    return db.session.get(User, int(id))
