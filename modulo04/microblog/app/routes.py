from flask import render_template, redirect, url_for, flash, request
from flask_login import (
    current_user, login_user, logout_user, login_required
)

from app import app
from app.alquimias import db
from app.models.models import User, Post


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    # Cria uma nova publicação quando o formulário é enviado
    if request.method == 'POST':
        body = request.form.get('body')
        if body:
            post = Post(body=body, author=current_user)
            db.session.add(post)
            db.session.commit()
            flash('Sua publicação está no ar!')
        return redirect(url_for('index'))

    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', title='Início', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Usuário já autenticado não precisa logar de novo
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash('Usuário ou senha inválidos.')
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('index'))

    return render_template('login.html', title='Login')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
