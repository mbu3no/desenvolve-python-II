from flask import Flask
from flask_login import LoginManager

from app.alquimias import db

# Objeto principal da aplicação
app = Flask(__name__)

# Chave secreta da aplicação (necessária para sessões e Flask-Login)
app.config['SECRET_KEY'] = "PD12345678"

# Banco de dados SQLite (criado dentro da pasta instance/)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///microblog.db'

# Inicializa o SQLAlchemy com a aplicação
db.init_app(app)

# Instancia o LoginManager (Flask-Login)
login = LoginManager(app)
# Rota para a qual usuários não autenticados são redirecionados
login.login_view = 'login'
login.login_message = "Por favor, faça login para acessar esta página."

# Importações ao final para evitar importação circular
from app import routes
from app.models import models
