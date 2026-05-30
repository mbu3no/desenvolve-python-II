"""Camada de acesso a dados (queries do SQLAlchemy).

Todas as funções de gerência de usuário retornam um objeto User (ou None),
conforme descrito na apostila.
"""
from datetime import datetime

from app import db
from app.models.models import User, Post


def validate_user_password(username, password):
    """Retorna o usuário se username existir e a senha conferir; senão None."""
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        return user
    return None


def user_exists(username):
    """Retorna o usuário com aquele username, ou None se não existir."""
    return User.query.filter_by(username=username).first()


def create_user(username, password, foto=None, bio=None, last_login=None):
    """Cria e persiste um novo usuário, retornando o objeto criado."""
    new_user = User(
        username=username,
        password=password,
        foto=foto,
        bio=bio,
        last_login=last_login or datetime.utcnow(),
    )
    db.session.add(new_user)
    db.session.commit()
    return new_user


def create_post(body, user):
    """Cria e persiste um novo post associado ao usuário informado."""
    post = Post(body=body, author=user, timestamp=datetime.utcnow())
    db.session.add(post)
    db.session.commit()
    return post


def get_timeline():
    """Retorna os 5 posts mais recentes, ordenados pelo timestamp (desc)."""
    return Post.query.order_by(Post.timestamp.desc()).limit(5).all()
