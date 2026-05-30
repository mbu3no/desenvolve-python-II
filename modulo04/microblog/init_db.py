"""Cria as tabelas no banco e cadastra um usuário de teste.

Execute uma única vez antes de rodar a aplicação:
    python init_db.py
"""
from app import app, db
from app.models.models import User

with app.app_context():
    db.create_all()

    # Cria um usuário de exemplo (admin / 1234) se ainda não existir
    if User.query.filter_by(username='admin').first() is None:
        u = User(username='admin', email='admin@microblog.com')
        u.set_password('1234')
        db.session.add(u)
        db.session.commit()
        print("Usuário 'admin' criado (senha: 1234).")
    else:
        print("Usuário 'admin' já existe.")

    print("Banco de dados pronto.")
