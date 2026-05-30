from app import app, db
from app.models.models import User, Post


@app.shell_context_processor
def make_shell_context():
    """Disponibiliza objetos no `flask shell` sem precisar importá-los."""
    return {'db': db, 'User': User, 'Post': Post}
