from flask import Flask
from flask_cors import CORS

from .models import db

def create_app(test_config=None):
    app = Flask(__name__)
    # Config par défaut
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///domus.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Si une config test est fournie, on l’utilise
    if test_config:
        app.config.update(test_config)
    CORS(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    from . import routes
    app.register_blueprint(routes.bp)
    return app