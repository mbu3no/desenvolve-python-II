from flask import render_template, redirect, url_for, request, flash
from flask_login import (
    current_user,    # objeto User atual
    login_user,      # método de login
    logout_user,     # método de logout
    login_required,  # decorador de rotas que exigem login
)

from app import app, alquimias


@app.route('/')
@login_required
def index():
    # Recupera o usuário autenticado e sua timeline (caso haja)
    user = None
    posts = None
    if current_user.is_authenticated:
        user = current_user
        posts = alquimias.get_timeline()
    return render_template('index.html', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = alquimias.validate_user_password(username, password)
        if user:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha inválidos.')

    return render_template('login.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        foto = request.form.get('foto')
        bio = request.form.get('bio')

        if alquimias.user_exists(username):
            flash('Este usuário já existe. Faça login.')
            return redirect(url_for('login'))

        user = alquimias.create_user(username, password, foto=foto, bio=bio)
        login_user(user)
        return redirect(url_for('index'))

    return render_template('cadastro.html')


@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    if request.method == 'POST':
        body = request.form.get('body')
        if body:
            alquimias.create_post(body, current_user)
        return redirect(url_for('index'))

    return render_template('post.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
