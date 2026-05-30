from datetime import datetime

from flask_login import UserMixin

from app import db, login


class User(UserMixin, db.Model):
    """Modelo de usuário.

    Herda de UserMixin (Flask-Login), que fornece is_authenticated,
    is_active, is_anonymous e get_id() usados internamente pela extensão.
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    # Campos adicionados na Parte 3 (incrementando o User)
    foto = db.Column(db.String(256))   # URL da foto de perfil
    bio = db.Column(db.String(280))    # breve descrição do usuário
    last_login = db.Column(db.DateTime, default=datetime.utcnow)

    # Relação 1:N -> um usuário tem vários posts.
    # backref='author' cria a referência reversa Post.author.
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'


class Post(db.Model):
    """Publicação textual do microblog (Parte 4)."""
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(280))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # Chave estrangeira apontando para users.id
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<Post {self.body}>'


@login.user_loader
def load_user(id):
    """Usada internamente pelo Flask-Login para recuperar o usuário atual
    a partir do id armazenado na sessão."""
    return db.session.get(User, int(id))
