from flask_sqlalchemy import SQLAlchemy

# Instância do SQLAlchemy isolada em seu próprio arquivo ("alquimias" = alchemy)
# para evitar importações circulares entre __init__.py, routes.py e models.py.
db = SQLAlchemy()
